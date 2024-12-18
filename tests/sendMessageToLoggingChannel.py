# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from botApp import botApp
from core.appConfig import LOGGING_CHANNEL_ID, TELEGRAM_OWNER_ID
from core.helpers.time import formatTime

print('LOGGING_CHANNEL_ID:', LOGGING_CHANNEL_ID)

timeStr = formatTime()

botApp.send_message(LOGGING_CHANNEL_ID, 'Test ' + timeStr)
