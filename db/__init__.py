import sys

IS_TEST = 'unittest' in sys.modules.keys()

if not IS_TEST:

    from ._init import openDb, closeDb, initDb
    from ._addCommand import addCommand
    from ._checkCommandExistsForMessageId import checkCommandExistsForMessageId
    from ._deleteCommandById import deleteCommandById
    from ._addTempMessage import addTempMessage

    from . import _types as types

    __all__ = [
        'openDb',
        'closeDb',
        'initDb',
        'addCommand',
        'checkCommandExistsForMessageId',
        'deleteCommandById',
        'addTempMessage',
        'types',
    ]
