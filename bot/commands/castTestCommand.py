# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from core.logger import getLogger
from bot.botApp import botApp

from .. import botConfig

from .castHelpers import demoVideo, downloadAndSendAudioToChat

_logger = getLogger('bot/commands/castTestCommand')


def castTestCommand(chat: telebot.types.Chat, message: telebot.types.Message):
    chatId = chat.id
    if not botConfig.TELEGRAM_OWNER_ID or botConfig.TELEGRAM_OWNER_ID != chatId:
        botApp.reply_to(message, 'Sorry you are not allowed to use this command.')
        return
    url = demoVideo
    _logger.info('castTestCommand: Start with url: %s' % url)
    # Let's start...
    downloadAndSendAudioToChat(url, chat, message)
