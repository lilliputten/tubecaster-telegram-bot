import sys

IS_TEST = 'unittest' in sys.modules.keys()
if not IS_TEST:
    from .commands import registerCommands
    from .requestFullAccess import requestFullAccess

    __all__ = [
        'registerCommands',
        'requestFullAccess',
    ]
