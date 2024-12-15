# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from core.logger import getLogger
from bot.botApp import botApp
from core.appConfig import TELEGRAM_OWNER_ID

from bot.cast import downloadAndSendAudioToChat
from bot.cast.castConfig import demoVideo


_logger = getLogger('bot/commands/castTestCommand')


def castTestCommand(chat: telebot.types.Chat, message: telebot.types.Message):
    chatId = chat.id
    if not TELEGRAM_OWNER_ID or TELEGRAM_OWNER_ID != chatId:
        botApp.reply_to(message, 'Sorry you are not allowed to use this command.')
        return
    url = demoVideo
    _logger.info('castTestCommand: Start with url: %s' % url)
    # Let's start...
    downloadAndSendAudioToChat(url, chat, message)
