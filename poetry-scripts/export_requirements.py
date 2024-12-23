import subprocess


def export_requirements():
    print('Exporting requirements...')
    cmd = [
        'poetry',
        'export',
        '-f',
        'requirements.txt',
        '--output',
        'requirements.txt',
        '--without-hashes',
    ]
    subprocess.run(cmd)
