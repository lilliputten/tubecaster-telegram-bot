from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from ._init import initDb
from .database import get_database_url, get_engine, load_db_env, reset_engine
from .models import Base


def get_admin_database_url() -> str:
    url = make_url(get_database_url(is_test=False))
    return url.set(database='postgres').render_as_string(hide_password=False)


def ensure_test_database() -> None:
    env = load_db_env()
    test_name = env.get('DB_TEST_NAME') or 'tubecaster_test'
    admin_engine = create_engine(get_admin_database_url(), isolation_level='AUTOCOMMIT', pool_pre_ping=True)
    try:
        with admin_engine.connect() as conn:
            exists = conn.execute(
                text('SELECT 1 FROM pg_database WHERE datname = :name'),
                {'name': test_name},
            ).scalar()
            if not exists:
                conn.execute(text(f'CREATE DATABASE "{test_name}"'))
    finally:
        admin_engine.dispose()


def setup_test_db():
    reset_engine()
    ensure_test_database()
    engine = get_engine(is_test=True)
    Base.metadata.create_all(engine)
    return initDb()


__all__ = [
    'ensure_test_database',
    'get_admin_database_url',
    'setup_test_db',
]
