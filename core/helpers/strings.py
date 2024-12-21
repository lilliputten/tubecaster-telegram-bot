import os


# Enable ansi colors for console output, see `ansiStyle`
_logAddStyle = True


if os.name == 'nt':
    try:
        __import__('colorama')
    except ImportError:
        _logAddStyle = False


def truncStr(s: str, maxLen: int):
    if len(s) >= maxLen - 1:
        s = s[: maxLen - 1] + '…'
    return s


def ansiStyle(value: str, *styles: str) -> str:
    if not _logAddStyle:
        return value

    codes = {
        'high': 0,
        'underline': 4,
        'bold': 1,
        # 'red': 31,
        # 'green': 32,
        # 'yellow': 33,
        # 'magenta': 35,
        # 'cyan': 36,
        #
        'black': 30,  # ???
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37,  # ???
    }

    for style in styles:
        value = f'\x1b[{codes[style]}m{value}'

    return f'{value}\x1b[0m'
