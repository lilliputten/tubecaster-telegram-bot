import subprocess


def upgrade():
    print('Alembic: upgrade head...')
    subprocess.run(['alembic', 'upgrade', 'head'], check=False)


def current():
    print('Alembic: current...')
    subprocess.run(['alembic', 'current'], check=False)
