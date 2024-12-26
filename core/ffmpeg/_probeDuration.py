import subprocess

from core.logger import getDebugLogger

from ._helpers import convertKwargsToCmdLineArgs


_logger = getDebugLogger()


def probeDuration(filename: str, **kwargs):
    cmd = 'ffprobe'
    # Create command...
    args = [
        cmd,  # A command to run
        '-show_packets',
    ]
    args += convertKwargsToCmdLineArgs(kwargs)
    args += ['-i', filename]
    # Run command...
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        errTitle = f'Error probing audio file duration ({cmd})'
        _logger.error(errTitle + ':\n' + err.decode('utf-8'))
        raise Exception(errTitle + ' (see error log output)')
    # TODO: Extract `dts_time` or `pts_time` value from the output
    s = out.decode('utf-8')
    findStr = 'ts_time='
    rpos = s.rfind(findStr)
    if rpos == -1:
        # Nothing found: to use another method?
        return 0
    startPos = rpos + len(findStr)
    endPos = s.find('\n', startPos)
    subStr = s[startPos:endPos]
    return float(subStr)
