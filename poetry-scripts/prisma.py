import subprocess
import os

from db._testDbConfig import testEnv

def format():
    print('Primsa: format...')
    cmd = [
        'prisma',
        'format',
    ]
    subprocess.run(cmd)


def db_push():
    print('Primsa: db push...')
    cmd = [
        'prisma',
        'db',
        'push',
        '--accept-data-loss',
    ]
    subprocess.run(cmd)

def db_push_test():
    os.environ['DATABASE_URL'] = testEnv['DATABASE_URL']
    print('Primsa: db push...')
    cmd = [
        'prisma',
        'db',
        'push',
    ]
    subprocess.run(cmd)

