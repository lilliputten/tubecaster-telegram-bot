import sys

IS_TEST = 'unittest' in sys.modules.keys()

if not IS_TEST:

    from .botApp import botApp

    __all__ = [
        'botApp',
    ]
