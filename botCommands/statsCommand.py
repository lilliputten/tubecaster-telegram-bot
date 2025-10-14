# -*- coding:utf-8 -*-

import traceback

import telebot  # pyTelegramBotAPI
from telebot import types
from telebot.states.sync.context import StateContext

from botApp import botApp
from botCast import sendStatsToChat
from botCore.constants import emojies
from botCore.helpers import getLanguageCode, getUserId, getUserName
from core.appConfig import TELEGRAM_OWNER_ID
from core.helpers.errors import errorToString
from core.logger import errorStyle, getDebugLogger, secondaryStyle, titleStyle, tretiaryStyle, warningTitleStyle
from core.utils import debugObj
from db import ensureValidUser

_logger = getDebugLogger()

_logTraceback = False


def statsCommand(chat: types.Chat, message: types.Message, state: StateContext):
    """
    Expects commands like:
    `/stats [ID]`
    """
    username = getUserName(message.from_user)
    text = message.text if message and message.text else ''
    args = text.strip().split()
    argsCount = len(args)
    userId = message.from_user.id if message.from_user else message.chat.id
    statsForUserId = userId
    isStatsCommand = args[0] == '/stats' if argsCount > 0 else False
    if isStatsCommand and argsCount > 1 and userId == TELEGRAM_OWNER_ID:
        statsForUserId = int(args[1])
    if not statsForUserId:
        botApp.reply_to(
            message,
            emojies.error + ' Invalid user id passed in "%s".' % text,
        )
        return
    # Wait for the url in the next message
    try:
        ensureValidUser(getUserId(message), username, getLanguageCode(message))
        sendStatsToChat(statsForUserId, chat.id, username, message)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = emojies.error + ' Error sending stats: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info(
                warningTitleStyle('statsCommand: Traceback for the following error:') + tretiaryStyle(sTraceback)
            )
        _logger.error(errorStyle('statsCommand: ' + errMsg))
        botApp.send_message(
            chat_id=chat.id,
            text=errMsg,
        )
    finally:
        _logger.info(titleStyle('statsCommand: Finished'))
