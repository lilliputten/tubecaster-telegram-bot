# -*- coding:utf-8 -*-

"""
Maintain simple logging features (to check logging system itself)
"""

# TODO: Move to `loggerConfig`?
useDebugLogs = True

# Local logs storage
debugLogs: list[str] = []


def getDebugLog():
    return '\n' + '\n'.join(debugLogs) + '\n'


def addDebugLog(s: str):
    debugLogs.append(s)


# Module exports...
__all__ = [
    'useDebugLogs',
    'getDebugLog',
    'addDebugLog',
]
