# -*- coding:utf-8 -*-


import telebot  # pyTelegramBotAPI

from core.appConfig import appConfig
from core.logger import getLogger


TELEGRAM_TOKEN = appConfig.get('TELEGRAM_TOKEN')

logger = getLogger('bot/botApp')

if not TELEGRAM_TOKEN:
    # NOTE: For the VDS environment this message will appear in a log file under the `/var/www/.uwsgi-apps/logs` folder
    errMsg = 'No telegram token defined'
    logger.error(errMsg)
    raise Exception(errMsg)

# @see: https://pypi.org/project/pyTelegramBotAPI/
# @see: https://pytba.readthedocs.io/en/latest/
botApp = telebot.TeleBot(token=TELEGRAM_TOKEN, threaded=False)

# @see https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/step_example.py
botApp.enable_save_next_step_handlers(delay=2)
botApp.load_next_step_handlers()

logger.info('botApp started with token: %s' % TELEGRAM_TOKEN)


# Module exports...
__all__ = [
    'botApp',
]
