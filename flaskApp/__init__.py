import sys

IS_TEST = 'unittest' in sys.modules.keys()

if not IS_TEST:

    from .flaskApp import flaskApp

    __all__ = [
        'flaskApp',
    ]
