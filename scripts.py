#!/usr/bin/env python3
"""
Poetry scripts runner - use this instead of poetry scripts for VSCode compatibility
Usage: python scripts.py <command>
"""
import subprocess
import sys


def export_requirements():
    print('Exporting requirements...')
    subprocess.run(['poetry', 'export', '-f', 'requirements.txt', '--output', 'requirements.txt', '--without-hashes'])


def lint():
    print('Running pyright linter...')
    subprocess.run(['pyright', '.'])


def format():
    print('Running python linter (blue)...')
    subprocess.run(['blue', '-q', '.'])


def isort():
    print('Running imports sorter...')
    subprocess.run(['isort', '--only-modified', '.'])


def check_all():
    isort()
    format()
    lint()


def db_upgrade():
    print('Alembic: upgrade head...')
    subprocess.run(['alembic', 'upgrade', 'head'])


def import_sqlite_db():
    from poetry_scripts.import_sqlite import main

    main()


commands = {
    'export_requirements': export_requirements,
    'isort': isort,
    'lint': lint,
    'format': format,
    'check_all': check_all,
    'db_upgrade': db_upgrade,
    'import_sqlite_db': import_sqlite_db,
}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Available commands:', ', '.join(commands.keys()))
        sys.exit(1)

    for command in sys.argv[1:]:
        if command in commands:
            commands[command]()
        else:
            print(f'Unknown command: {command}')
            print('Available commands:', ', '.join(commands.keys()))
            sys.exit(1)
