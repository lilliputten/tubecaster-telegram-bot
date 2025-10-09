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


def check_all():
    print('Running imports sorter...')
    subprocess.run(['isort', '--only-modified', '.'])
    format()
    lint()


def prisma_format():
    print('Prisma: format...')
    subprocess.run(['prisma', 'format'])


def prisma_format_and_validate():
    prisma_format()
    print('Prisma: validate...')
    subprocess.run(['prisma', 'validate'])


def prisma_db_push():
    print('Prisma: db push...')
    subprocess.run(['prisma', 'db', 'push'])


def prisma_db_push_test():
    import os

    os.environ['DATABASE_URL'] = 'file:.test.db'
    print('Prisma: db push test...')
    subprocess.run(['prisma', 'db', 'push'])


def prisma_db_push_all():
    prisma_db_push()
    prisma_db_push_test()


commands = {
    'export_requirements': export_requirements,
    'lint': lint,
    'format': format,
    'check_all': check_all,
    'prisma_format': prisma_format,
    'prisma_format_and_validate': prisma_format_and_validate,
    'prisma_db_push': prisma_db_push,
    'prisma_db_push_test': prisma_db_push_test,
    'prisma_db_push_all': prisma_db_push_all,
}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Available commands:', ', '.join(commands.keys()))
        sys.exit(1)

    command = sys.argv[1]
    if command in commands:
        commands[command]()
    else:
        print(f'Unknown command: {command}')
        print('Available commands:', ', '.join(commands.keys()))
