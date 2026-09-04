import os
from typing import Optional
from urllib.parse import quote_plus

from dotenv import dotenv_values
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

_engine: Optional[Engine] = None
_SessionFactory: Optional[scoped_session[Session]] = None


def load_db_env() -> dict[str, str]:
    values: dict[str, str] = {}
    for name in ('.env', '.env.server', '.env.local'):
        loaded = dotenv_values(name)
        for key, value in loaded.items():
            if value is not None:
                values[key] = value
    for key, value in os.environ.items():
        values[key] = value
    return values


def is_test_runtime() -> bool:
    env = load_db_env()
    return env.get('DB_USE_TEST', '').lower() in ('1', 'true', 'yes')


def get_db_name(is_test: Optional[bool] = None) -> str:
    env = load_db_env()
    use_test = is_test_runtime() if is_test is None else is_test
    if use_test:
        return env.get('DB_TEST_NAME') or 'tubecaster_test'
    return env.get('DB_NAME') or 'tubecaster'


def get_database_url(is_test: Optional[bool] = None) -> str:
    env = load_db_env()
    user = env.get('DB_USER') or 'postgres'
    password = env.get('DB_PASSWORD') or ''
    host = env.get('DB_HOST') or 'localhost'
    port = env.get('DB_PORT') or '5432'
    name = get_db_name(is_test=is_test)
    return f'postgresql+psycopg2://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{name}'


def get_engine(is_test: Optional[bool] = None) -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(
            get_database_url(is_test=is_test),
            pool_pre_ping=True,
        )
    return _engine


def get_session_factory(is_test: Optional[bool] = None) -> scoped_session[Session]:
    global _SessionFactory
    if _SessionFactory is None:
        _SessionFactory = scoped_session(
            sessionmaker(
                bind=get_engine(is_test=is_test),
                autoflush=True,
                autocommit=False,
                expire_on_commit=False,
            )
        )
    return _SessionFactory


def close_sessions() -> None:
    if _SessionFactory is not None:
        _SessionFactory.remove()


def reset_engine() -> None:
    global _engine, _SessionFactory
    close_sessions()
    if _SessionFactory is not None:
        _SessionFactory = None
    if _engine is not None:
        _engine.dispose()
        _engine = None


__all__ = [
    'close_sessions',
    'get_database_url',
    'get_db_name',
    'get_engine',
    'get_session_factory',
    'is_test_runtime',
    'load_db_env',
    'reset_engine',
]
