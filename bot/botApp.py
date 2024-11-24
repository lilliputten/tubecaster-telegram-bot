# -*- coding:utf-8 -*-

#  import traceback
#  from telegram import Update
#  from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import telebot  # pytelegrambotapi

from core.appConfig import appConfig

#  from core.helpers.errors import errorToString
#  from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger

# @see https://python-telegram-bot.org/
# @see https://docs.python-telegram-bot.org/

TELEGRAM_TOKEN = appConfig.get('TELEGRAM_TOKEN')

if not TELEGRAM_TOKEN:
    raise Exception('No telegram token defined')

#  changed = appConfig.get('changed')

logger = getLogger('bot/botApp')

logger.info('Token: %s' % TELEGRAM_TOKEN)

botApp = telebot.TeleBot(token=TELEGRAM_TOKEN, threaded=False)


# Module exports...
__all__ = [
    'botApp',
]
