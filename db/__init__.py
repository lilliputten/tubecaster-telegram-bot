import sys

IS_TEST = 'unittest' in sys.modules.keys()

if not IS_TEST:

    from . import _types as types

    from ._init import openDb, closeDb, initDb
    from ._addCommand import addCommand
    from ._checkCommandExistsForMessageId import checkCommandExistsForMessageId
    from ._deleteCommandById import deleteCommandById
    from ._addTempMessage import addTempMessage
    from ._getTempMessagesForCommand import getTempMessagesForCommand

    __all__ = [
        'types',
        'openDb',
        'closeDb',
        'initDb',
        'addCommand',
        'checkCommandExistsForMessageId',
        'deleteCommandById',
        'addTempMessage',
        'getTempMessagesForCommand',
    ]
