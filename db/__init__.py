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
    from ._deleteOutdatedCommands import deleteOutdatedCommands
    from ._deleteOutdatedTempMessages import deleteOutdatedTempMessages
    from ._findUser import findUser
    from ._addActiveUser import addActiveUser
    from ._updateStats import updateStats
    from ._collectStats import collectStats

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
        'deleteOutdatedCommands',
        'deleteOutdatedTempMessages',
        'findUser',
        'addActiveUser',
        'updateStats',
        'collectStats',
    ]
