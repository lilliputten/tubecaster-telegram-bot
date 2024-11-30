# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
import traceback

from core.helpers.errors import errorToString

#  from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger

#  from core.appConfig import appConfig

from bot.botApp import botApp

#  from core.utils import debugObj

from .. import botConfig

from .castHelpers import demoVideo, downloadAndSendAudioToChat

_logger = getLogger('bot/commands/castTestCommand')

_logTraceback = False


@botApp.message_handler(commands=['castTest'])
def castTestCommand(message: telebot.types.Message):
    # Get core parameters
    chat = message.chat
    chatId = chat.id
    if not botConfig.TELEGRAM_OWNER_ID or botConfig.TELEGRAM_OWNER_ID != chatId:
        botApp.reply_to(message, 'Sorry you are not allowed to use this command.')
        return
    url = demoVideo   # args[1]
    # Let's start...
    try:
        downloadAndSendAudioToChat(url, message)   # username, chatId)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'Error fetching audio: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('castTestCommand: Traceback for the following error:' + sTraceback)
        _logger.error('castTestCommand: ' + errMsg)
        botApp.reply_to(message, errMsg)


__all__ = [
    'castTestCommand',
]
