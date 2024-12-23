import subprocess


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


# def test():
#     # NOTE: It doesn't work as poetry hasn't invoked it under the venv environment
#     # TODO: Run in a less com;ex way?
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
