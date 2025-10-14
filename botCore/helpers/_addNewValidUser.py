import traceback

import telebot  # pyTelegramBotAPI
from telebot import types

from botApp import botApp
from botCore.constants import emojies
from botCore.helpers._replyOrSend import replyOrSend
from core.helpers import errorToString
from core.helpers.time import getCurrentDateTime
from core.logger import errorStyle, getDebugLogger, secondaryStyle, titleStyle, warningStyle
from db import ensureValidUser, updateUserStatus

_logger = getDebugLogger()

_logTraceback = False


def addNewValidUser(userId: int, userStr: str, languageCode: str | None, query: types.CallbackQuery):
    message = query.message  # <types.Message object at 0x000002B8D6F12210>
    chatId = message.chat.id
    try:
        user = ensureValidUser(userId, userStr, languageCode)
        now = getCurrentDateTime()
        userStatus = updateUserStatus(
            userId,
            {
                'userMode': 'FREE',
                'statusChangedAt': now,
            },
        )
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
        replyOrSend(emojies.robot + ' ' + errMsg, chatId)  # , message)
