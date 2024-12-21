# -*- coding:utf-8 -*-

import sys
import telebot  # pyTelegramBotAPI

from core.appConfig import TELEGRAM_TOKEN
from core.logger import getDebugLogger, secondaryStyle, errorStyle, titleStyle
from core.utils import debugObj


IS_TEST = 'unittest' in sys.modules.keys()

_logger = getDebugLogger()


def showDebug():
    debugItems = {
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
    }
    logItems = [
        titleStyle('botApp started'),
        secondaryStyle(debugObj(debugItems)),
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
        _logger.error(errorStyle(errMsg))
        raise Exception(errMsg)

    # @see: https://pypi.org/project/pyTelegramBotAPI/
    # @see: https://pytba.readthedocs.io/en/latest/
    botApp = telebot.TeleBot(token=TELEGRAM_TOKEN, threaded=False)

    # # @see https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/step_example.py
    # botApp.enable_save_next_step_handlers(delay=2)
    #
    # # XXX: This line causes an error:
    # # AttributeError: partially initialized module 'botApp.botApp' has no attribute 'message_handler' (most likely due to a circular import)
    # botApp.load_next_step_handlers()

    return botApp


if not IS_TEST:
    botApp = startBotApp()


__all__ = [
    'botApp',
]
