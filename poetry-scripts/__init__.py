import subprocess

from .export_requirements import export_requirements


def lint():
    print('Running pyright linter...')
    cmd = [
        'pyright',
        '.',
    ]
    subprocess.run(cmd)


def format():
    print('Running python linter (blue)...')
    cmd = [
        'blue',
        '.',
    ]
    subprocess.run(cmd)


def check_all():
    format()
    lint()
