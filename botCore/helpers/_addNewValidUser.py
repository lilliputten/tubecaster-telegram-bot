import traceback
import telebot  # pyTelegramBotAPI
from telebot.states.sync.context import StateContext

from core.appConfig import CONTROLLER_CHANNEL_ID, LOCAL, PROJECT_INFO, PROJECT_PATH
from core.helpers.errors import errorToString
from core.helpers.strings import removeAnsiStyles
from core.helpers.time import formatTime, getTimeStamp
from core.logger import getDebugLogger, titleStyle, secondaryStyle
from core.logger.utils import errorStyle, warningStyle
from core.utils import debugObj

from db import addActiveUser

from botCore.constants import stickers, emojies
from botCore.helpers import createSendRegistrationReguestButtonsMarkup
from botCore.helpers import getUserName
from botCore.helpers._replyOrSend import replyOrSend

from botApp import botApp

_logger = getDebugLogger()

_logTraceback = False


def addNewValidUser(newUserId: int, newUserStr: str, query: telebot.types.CallbackQuery):
    message = query.message  # <telebot.types.Message object at 0x000002B8D6F12210>
    chatId = message.chat.id
    try:
        return addActiveUser(newUserId, newUserStr)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error adding new user: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle(titleStyle('Traceback for the following error:') + sTraceback))
        _logger.error(errorStyle('addNewValidUser: ' + errMsg))
        replyOrSend(botApp, emojies.robot + ' ' + errMsg, chatId)   # , message)
