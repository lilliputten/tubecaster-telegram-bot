# import sys
# IS_TEST = 'unittest' in sys.modules.keys()
# if not IS_TEST:

from . import _types as types
from ._init import openDb, closeDb, initDb

from ._addCommand import addCommand
from ._addTempMessage import addTempMessage
from ._checkCommandExistsForMessageId import checkCommandExistsForMessageId
from ._deleteCommandById import deleteCommandById
from ._deleteOutdatedCommands import deleteOutdatedCommands
from ._deleteOutdatedTempMessages import deleteOutdatedTempMessages
from ._getTempMessagesForCommand import getTempMessagesForCommand

from .stats import collectStats, getCurrentMonthStats, getMonthlyStats, getTotalStats, updateStats

from .status import getUserStatus

from .user import addActiveUser, findUser, getActiveUser, updateUserStatus, wipeOutDeletedUsers

__all__ = [
    # core
    'types',
    'openDb',
    'closeDb',
    'initDb',
    # common
    'addCommand',
    'addTempMessage',
    'checkCommandExistsForMessageId',
    'collectStats',
    'deleteCommandById',
    'deleteOutdatedCommands',
    'deleteOutdatedTempMessages',
    'getTempMessagesForCommand',
    # stats
    'collectStats',
    'getCurrentMonthStats',
    'getMonthlyStats',
    'getTotalStats',
    'updateStats',
    # status
    'getUserStatus',
    # user
    'addActiveUser',
    'findUser',
    'getActiveUser',
    'updateUserStatus',
    'wipeOutDeletedUsers',
]
