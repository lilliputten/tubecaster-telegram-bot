# -*- coding:utf-8 -*-

import traceback
import telebot  # pyTelegramBotAPI
from functools import partial

from core.helpers.errors import errorToString
from core.helpers.urls import isYoutubeLink
from core.logger import getDebugLogger, titleStyle, secondaryStyle, tretiaryStyle, errorStyle, warningTitleStyle
from core.utils import debugObj

from botApp import botApp
from botCore.helpers import getUserName
from botCore.helpers import replyOrSend
from botCore.constants import emojies
from botCast import sendInfoToChat


_logger = getDebugLogger()

_logTraceback = False


def infoForUrlStep(chat: telebot.types.Chat, message: telebot.types.Message):
    _logger.info('infoForUrlStep: Before')
    try:
        text = message.text
        chatId = chat.id
        username = getUserName(message.from_user)
        if not text:
            botApp.reply_to(message, 'Video url is expected.')
            return
        url = text
        if not isYoutubeLink(url):
            botApp.reply_to(message, emojies.error + ' A youtube url has been expected. But you have sent "%s"' % url)
            return
        obj = {
            'url': url,
            'chatId': chatId,
            'username': username,
        }
        debugStr = debugObj(obj)
        logItems = [
            titleStyle('infoForUrlStep: Start'),
            secondaryStyle(debugStr),
        ]
        logContent = '\n'.join(logItems)
        _logger.info(logContent)
        sendInfoToChat(url, chat.id, username, message)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = emojies.error + ' Error fetching a video info: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info(
                warningTitleStyle('infoForUrlStep: Traceback for the following error:') + tretiaryStyle(sTraceback)
            )
        _logger.error(errorStyle('infoForUrlStep: ' + errMsg))
        botApp.send_message(
            chat_id=chat.id,
            text=errMsg,
        )


def infoCommand(chat: telebot.types.Chat, message: telebot.types.Message):
    username = getUserName(message.from_user)
    text = message.text if message and message.text else ''
    args = text.strip().split()
    argsCount = len(args)
    if argsCount > 2:
        botApp.reply_to(message, emojies.error + ' Too many arguments.')
        return
    isInfoCommand = args[0] == '/info' if argsCount > 0 else False
    if not argsCount or (isInfoCommand and argsCount == 1):
        replyMsg = emojies.question + ' Ok, now send the video address:'
        replyOrSend(botApp, replyMsg, chat.id, message)
        _logger.info('infoCommand: Registering the next handler with infoForUrlStep')
        botApp.register_next_step_handler_by_chat_id(chat.id, partial(infoForUrlStep, chat))
        return
    url = args[0]
    if isInfoCommand and argsCount == 2:
        url = args[1]
    if not isYoutubeLink(url):
        botApp.reply_to(message, emojies.error + ' A youtube url has been expected. But you have sent "%s"' % url)
        return
    # Wait for the url
    try:
        sendInfoToChat(url, chat.id, username, message)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = emojies.error + ' Error fetching a video info: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info(
                warningTitleStyle('infoCommand: Traceback for the following error:') + tretiaryStyle(sTraceback)
            )
        _logger.error(errorStyle('infoCommand: ' + errMsg))
        botApp.send_message(
            chat_id=chat.id,
            text=errMsg,
        )
        #  raise Exception(errMsg)
    finally:
        _logger.info(titleStyle('infoCommand: Finished'))

