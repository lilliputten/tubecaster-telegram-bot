import subprocess


def run():
    print('Running pyright linter...')
    cmd = [
        'pyright',
        '.',
    ]
    subprocess.run(cmd)
