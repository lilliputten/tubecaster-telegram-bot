import json
import subprocess

from core.logger import getDebugLogger, titleStyle, secondaryStyle

from ._helpers import convertKwargsToCmdLineArgs


_logger = getDebugLogger()


def probe(filename: str, **kwargs):
    cmd = 'ffprobe'
    # Create command...
    args = [
        cmd,  # A command to run
        '-show_format',  # Show format
        '-show_streams',  # Show streams
        '-of',
        'json',  # Use json format
    ]
    args += convertKwargsToCmdLineArgs(kwargs)
    args += [filename]
    # Run command...
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        errTitle = f'Error probing audio file ({cmd})'
        _logger.error(errTitle + ':\n' + err.decode('utf-8'))
        raise Exception(errTitle + ' (see error log output)')
        #  raise Error(cmd, out, err)
    return json.loads(out.decode('utf-8'))
