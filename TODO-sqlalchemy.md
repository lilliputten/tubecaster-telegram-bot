# Replace Prisma (SQLite) with SQLAlchemy (PostgreSQL)

Status legend: `[ ]` pending, `[~]` in progress, `[x]` done.

## 1. Inventory and plan

- [x] Inspect `prisma/schema.prisma`, `db/`, `poetry_scripts/`, and root config/env files only
- [x] Record Prisma models, query modules, tests, and env usage
- [x] Create this TODO file

## 2. Packages and virtualenv

- [x] Remove `prisma` from Poetry
- [x] Add `sqlalchemy`, `alembic`, `psycopg2-binary`
- [x] Update `pyproject.toml` scripts (drop Prisma, add migration/import helpers)
- [x] Sync the local venv (`poetry lock` / `poetry install`)
- [x] Export `requirements.txt` for the production raw venv

## 3. Environment configuration

- [x] Remove unused `DATABASE_URL` from `.env.local.SAMPLE` and `.env.server.SAMPLE`
- [x] Add PostgreSQL variables (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_TEST_NAME`)
- [x] Keep existing `.env.local` PostgreSQL placeholders (`tubecaster` / `postgres`)
- [x] Confirm `.env` has no database-related parameters

## 4. SQLAlchemy models and connection

- [x] Translate Prisma schema to SQLAlchemy models (`db/models.py`)
- [x] Add engine URL builder and cached engine / session factory (`db/database.py`)
- [x] Update `db/_init.py` (`openDb` / `initDb` / `closeDb`) with cached engine (not a shared Session)
- [x] Update `db/_types.py` and `db/_testDbConfig.py`

## 5. Alembic

- [x] Initialize Alembic (`alembic.ini`, `alembic/`)
- [x] Point `env.py` at SQLAlchemy metadata and `DB_*` connection settings
- [x] Add the initial migration matching the Prisma tables/indexes/FKs

## 6. Rewrite queries

- [ ] Command / temp-message routines (`db/_addCommand.py`, `_addTempMessage.py`, etc.)
- [ ] User / status / stats routines
- [ ] Keep existing function signatures where possible
- [ ] Replace leftover Prisma usage in bot command handlers (types + `initDb()` client API)

## 7. Tests

- [ ] Rewrite `db/*_test.py` to use SQLAlchemy sessions/models
- [ ] Point tests at `DB_TEST_NAME` (default `tubecaster_test`)

## 8. Prisma cleanup

- [ ] Remove `poetry_scripts/prisma.py` and Prisma Poetry/npm/scripts helpers
- [ ] Keep `prisma/schema.prisma` and Prisma migrations
- [ ] Keep untracked SQLite data (`prisma/.data.db` and similar)

## 9. SQLite import script

- [x] Add a script to copy `prisma/.data.db` tables into PostgreSQL
- [ ] Preserve table order, types, sequences, and cascade-safe FKs

## 10. Lint and tests

- [ ] Run `poetry run lint` and fix errors
- [ ] Run `poetry run python -m unittest discover -v -f -t . -s . -p "*_test.py"`
- [ ] Apply Alembic migrations to local/test databases as needed
