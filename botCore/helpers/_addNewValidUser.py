import traceback
import telebot  # pyTelegramBotAPI

from core.helpers import errorToString
from core.logger import getDebugLogger, titleStyle, secondaryStyle, errorStyle, warningStyle

from db import addActiveUser

from botCore.constants import emojies
from botCore.helpers._replyOrSend import replyOrSend

from botApp import botApp

from db.user import updateUserStatus

_logger = getDebugLogger()

_logTraceback = False


def addNewValidUser(userId: int, userStr: str, languageCode: str | None, query: telebot.types.CallbackQuery):
    message = query.message  # <telebot.types.Message object at 0x000002B8D6F12210>
    chatId = message.chat.id
    try:
        user = addActiveUser(userId, userStr, languageCode)
        userStatus = updateUserStatus(userId, 'FREE')
        if user and userStatus:
            user.userStatus = userStatus
        return user
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
