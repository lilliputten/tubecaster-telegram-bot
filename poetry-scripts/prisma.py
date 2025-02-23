import subprocess
import os

from db._testDbConfig import testEnv

"""
NOTE: It's probably better to use `sh .venv-scripts/prisma-init.sh` (under venv) manually due to prisma/poetry misunderstanding:

```
. ./.venv/Scripts/activate
sh .venv-scripts/prisma-init.sh
deactivate
"""


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
