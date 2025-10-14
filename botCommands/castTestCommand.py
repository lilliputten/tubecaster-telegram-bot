# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
from telebot import types

from botApp import botApp
from botCast import downloadAndSendAudioToChat
from botCast.config import demoVideo
from botCore.helpers import getLanguageCode, getUserId, getUserName
from core.appConfig import TELEGRAM_OWNER_ID
from core.logger import getDebugLogger, secondaryStyle, titleStyle
from db import ensureValidUser

_logger = getDebugLogger()


def castTestCommand(chat: types.Chat, message: types.Message):
    chatId = chat.id
    username = getUserName(message.from_user)
    # userId = message.from_user.id
    if not TELEGRAM_OWNER_ID or TELEGRAM_OWNER_ID != chatId:
        botApp.reply_to(message, 'Sorry you are not allowed to use this command.')
        return
    url = demoVideo
    _logger.info('castTestCommand: Start with url: %s' % url)
    # Let's start...
    ensureValidUser(getUserId(message), username, getLanguageCode(message))
    downloadAndSendAudioToChat(url, chatId, username, message)
