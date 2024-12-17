# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from botApp import botApp
from core.appConfig import LOGGING_CHANNEL_ID, TELEGRAM_OWNER_ID

print('LOGGING_CHANNEL_ID:', LOGGING_CHANNEL_ID)

botApp.send_message(LOGGING_CHANNEL_ID, 'Test')
