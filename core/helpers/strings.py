import os


# Enable ansi colors for console output, see `ansiStyle`
_logAddStyle = True


if os.name == 'nt':
    try:
        __import__('colorama')
    except ImportError:
        _logAddStyle = False


def truncStr(str: str, maxLen: int):
    if len(str) >= maxLen - 1:
        str = str[: maxLen - 1] + '…'
    return str


def ansiStyle(value: str, *styles: str) -> str:
    if not _logAddStyle:
        return value

    codes = {
        'bold': 1,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'magenta': 35,
        'cyan': 36,
    }

    for style in styles:
        value = f'\x1b[{codes[style]}m{value}'

    return f'{value}\x1b[0m'
