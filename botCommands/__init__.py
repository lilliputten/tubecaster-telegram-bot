import sys
IS_TEST = 'unittest' in sys.modules.keys()
if not IS_TEST:
    from .commands import registerCommands
    __all__ = ['registerCommands']
