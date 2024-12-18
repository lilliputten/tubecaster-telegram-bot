# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from core.logger import getLogger
from core.appConfig import TELEGRAM_OWNER_ID

from botApp import botApp
from botCast import downloadAndSendAudioToChat
from botCast.config import demoVideo


_logger = getLogger('botCommands/castTestCommand')


def castTestCommand(chat: telebot.types.Chat, message: telebot.types.Message):
    chatId = chat.id
    username = str(chat.username)
    if not TELEGRAM_OWNER_ID or TELEGRAM_OWNER_ID != chatId:
        botApp.reply_to(message, 'Sorry you are not allowed to use this command.')
        return
    url = demoVideo
    _logger.info('castTestCommand: Start with url: %s' % url)
    # Let's start...
    downloadAndSendAudioToChat(url, chatId, username, message)
