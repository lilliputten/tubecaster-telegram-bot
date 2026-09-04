"""Import Prisma SQLite data (`prisma/.data.db`) into PostgreSQL."""

from __future__ import annotations

import argparse
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dateutil import parser as date_parser
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from db.database import get_database_url
from db.models import Command, MonthlyStats, TempMessage, TotalStats, User, UserStatus

DEFAULT_SQLITE_PATH = Path('prisma') / '.data.db'

TABLE_MODELS = {
    'Users': User,
    'Commands': Command,
    'TempMessages': TempMessage,
    'UserStatus': UserStatus,
    'TotalStats': TotalStats,
    'MonthlyStats': MonthlyStats,
}

# Parent tables first so foreign keys succeed.
IMPORT_ORDER = [
    'Users',
    'Commands',
    'TempMessages',
    'UserStatus',
    'TotalStats',
    'MonthlyStats',
]

BOOLEAN_COLUMNS = {'isDeleted', 'isActive'}
DATETIME_COLUMNS = {
    'createdAt',
    'updatedAt',
    'deletedAt',
    'statusChangedAt',
    'paidAt',
    'paymentValidUntil',
}


def parse_datetime(value: Any) -> datetime | None:
    if value is None or value == '':
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value

    # Check if the value is a large number that looks like a millisecond timestamp
    numeric_val = None
    if isinstance(value, (int, float)):
        numeric_val = value
    elif isinstance(value, str):
        try:
            numeric_val = float(value)
        except ValueError:
            # If conversion fails, it's a normal string, proceed with original value as string
            pass

    if numeric_val is not None and abs(numeric_val) >= 1700000000000:   # Threshold for year 2024+ in milliseconds
        # Assume it's a millisecond timestamp and convert to seconds for datetime.fromtimestamp
        timestamp_seconds = numeric_val / 1_000.0   # Divide by 1000 to convert milliseconds to seconds
        try:
            return datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)
        except (OSError, ValueError, OverflowError) as e:
            # If conversion fails (e.g., timestamp out of range), log and return None
            print(f'Warning: Could not convert timestamp {numeric_val} to datetime ({e})')
            return None

    # If not a large number, treat as a standard date string
    processed_value = str(value)

    # Final check: if processed_value is a string representation of a large number (millisecond timestamp),
    # treat it to avoid dateutil parser overflow.
    try:
        parsed_float = float(processed_value)
        if abs(parsed_float) >= 1700000000000:   # Threshold for year 2024+ in milliseconds
            # Assume it's a millisecond timestamp and convert to seconds
            timestamp_seconds = parsed_float / 1_000.0   # Divide by 1000 to convert milliseconds to seconds
            try:
                return datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)
            except (OSError, ValueError, OverflowError) as e:
                print(
                    f"Warning: Could not convert timestamp {parsed_float} (from string '{processed_value}') to datetime ({e})"
                )
                return None
    except ValueError:
        # If it's not a numeric string, it's safe to pass to the date parser
        pass

    # Wrap the parser call in a try-except to catch any remaining OverflowErrors
    try:
        parsed = date_parser.parse(processed_value)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed
    except OverflowError:
        # If an OverflowError occurs here, it means a very large number slipped through our checks.
        # Log the problematic value and return None.
        print(f"Warning: OverflowError parsing datetime value '{processed_value}'. Skipping.")
        return None


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in ('1', 'true', 't', 'yes')


def convert_row(table: str, row: dict[str, Any]) -> dict[str, Any]:
    converted: dict[str, Any] = {}
    model = TABLE_MODELS[table]
    column_names = set(model.__table__.columns.keys())
    for key, value in row.items():
        if key not in column_names:
            continue
        if key in BOOLEAN_COLUMNS:
            converted[key] = parse_bool(value)
        elif key in DATETIME_COLUMNS:
            converted[key] = parse_datetime(value)
        else:
            converted[key] = value
    return converted


def fetch_sqlite_rows(sqlite_path: Path, table: str) -> list[dict[str, Any]]:
    connection = sqlite3.connect(sqlite_path)
    connection.row_factory = sqlite3.Row
    try:
        cursor = connection.execute(f'SELECT * FROM "{table}"')
        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()


def sqlite_tables(sqlite_path: Path) -> set[str]:
    connection = sqlite3.connect(sqlite_path)
    try:
        cursor = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '_prisma%'"
        )
        return {row[0] for row in cursor.fetchall()}
    finally:
        connection.close()


def reset_sequences(engine: Engine) -> None:
    statements = [
        """
        SELECT setval(
            pg_get_serial_sequence('"Commands"', 'id'),
            COALESCE((SELECT MAX(id) FROM "Commands"), 1),
            true
        )
        """,
        """
        SELECT setval(
            pg_get_serial_sequence('"TempMessages"', 'id'),
            COALESCE((SELECT MAX(id) FROM "TempMessages"), 1),
            true
        )
        """,
    ]
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


def import_sqlite(sqlite_path: Path, database_url: str | None = None) -> None:
    if not sqlite_path.exists():
        raise FileNotFoundError(f'SQLite database not found: {sqlite_path}')

    engine = create_engine(database_url or get_database_url(), pool_pre_ping=True)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    available = sqlite_tables(sqlite_path)
    session = session_factory()
    try:
        for table in IMPORT_ORDER:
            if table not in available:
                print(f'Skip missing SQLite table: {table}')
                continue
            rows = fetch_sqlite_rows(sqlite_path, table)
            model = TABLE_MODELS[table]
            imported = 0
            for row in rows:
                payload = convert_row(table, row)
                session.merge(model(**payload))
                imported += 1
            session.commit()
            print(f'Imported {imported} row(s) into {table}')
        reset_sequences(engine)
        print('Sequence values updated.')
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description='Import Prisma SQLite data into PostgreSQL')
    parser.add_argument(
        '--sqlite',
        default=str(DEFAULT_SQLITE_PATH),
        help='Path to the Prisma SQLite file (default: prisma/.data.db)',
    )
    parser.add_argument(
        '--database-url',
        default=None,
        help='Optional SQLAlchemy PostgreSQL URL. Defaults to DB_* environment settings.',
    )
    args = parser.parse_args()
    import_sqlite(Path(args.sqlite), args.database_url)


if __name__ == '__main__':
    main()
