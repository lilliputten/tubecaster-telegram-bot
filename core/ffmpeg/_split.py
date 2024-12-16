import subprocess

from core.logger import getLogger

from ._helpers import convertKwargsToCmdLineArgs


_logger = getLogger('core/ffmpeg/_split')


def split(filename: str, outFilename: str, start: float, end: float, format='mp4', **kwargs):
    cmd = 'ffmpeg'
    # Create command...
    # fmt: off
    args = [
        cmd,  # A command to run
        '-i', filename,  # Input file
        '-vn',  # No video
        '-acodec', 'copy',  # Just copy
        '-ss', str(start),  # From (seconds)
        '-to', str(end),  # To (seconds)
        '-y',  # Override file
        '-f', format,  # Use mp4 format
    ]
    # fmt: on
    args += convertKwargsToCmdLineArgs(kwargs)
    args += [outFilename]
    # Run command...
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        errTitle = f'Error splitting audio file ({cmd})'
        _logger.error(errTitle + ':\n' + err.decode('utf-8'))
        raise Exception(errTitle + ' (see error log output)')
        #  raise Error(cmd, out, err)
    return out.decode('utf-8')
