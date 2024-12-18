# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from core.appConfig import LOCAL, TELEGRAM_TOKEN, PROJECT_INFO
from core.helpers.runtime import getModPath
from core.logger import getLogger
from core.utils import debugObj


_logger = getLogger(getModPath())


def showDebug():
    debugItems = {
        'PROJECT_INFO': PROJECT_INFO,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'LOCAL': LOCAL,
    }
    logItems = [
        'botApp started',
        debugObj(debugItems),
    ]
    logContent = '\n'.join(logItems)
    _logger.info(logContent)


def startBotApp():
    """
    Start the telegram bot application.
    """

    showDebug()

    if not TELEGRAM_TOKEN:
        # NOTE: For the VDS environment this message will appear in a log file under the `/var/www/.uwsgi-apps/logs` folder
        errMsg = 'No telegram token defined'
        _logger.error(errMsg)
        raise Exception(errMsg)

    # @see: https://pypi.org/project/pyTelegramBotAPI/
    # @see: https://pytba.readthedocs.io/en/latest/
    botApp = telebot.TeleBot(token=TELEGRAM_TOKEN, threaded=False)

    # @see https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/step_example.py
    botApp.enable_save_next_step_handlers(delay=2)
    botApp.load_next_step_handlers()

    return botApp


botApp = startBotApp()


__all__ = [
    'botApp',
]
