import os
import subprocess


def isort():
    print('Running imports sorter...')
    cmd = [
        'isort',
        '--only-modified',
        '.',
    ]
    subprocess.run(cmd)


def lint():
    print('Running pyright linter...')
    # Disable version check (is that a correct way?)
    env = os.environ.copy()
    env['PYRIGHT_PYTHON_FORCE_VERSION'] = '1.1.403'
    cmd = [
        'pyright',
        '.',
    ]
    subprocess.run(cmd, env=env)


def format():
    print('Running python linter (blue)...')
    cmd = [
        'blue',
        '.',
    ]
    subprocess.run(cmd)


def check_all():
    isort()
    format()
    lint()


# def test():
#     # NOTE: It doesn't work as poetry hasn't invoked it under the venv environment
#     # TODO: Run in a less complex way? Run from the cli: poetry run python -m unittest discover -v -p "*_test.py"
#     print('Running unittest tests...')
#     cmd = [
#         'python',
#         '-m',
#         'unittest',
#         'discover',
#         '-v',
#         '-f',
#         '-t',
#         '.',
#         '-s',
#         '.',
#         '-p',
#         '*_test.py',
#     ]
#     subprocess.run(cmd)
