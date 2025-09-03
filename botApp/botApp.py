# -*- coding:utf-8 -*-

import sys

import telebot  # pyTelegramBotAPI
from telebot import custom_filters
from telebot.storage import (
    StateMemoryStorage,
)  # TODO: To use production-ready storage, like StateDataContext, StateStorageBase, etc?

from core.appConfig import TELEGRAM_TOKEN
from core.logger import errorStyle, getDebugLogger, secondaryStyle, titleStyle
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

    state_storage = StateMemoryStorage()  # don't use this in production; switch to redis

    # @see: https://pypi.org/project/pyTelegramBotAPI/
    # @see: https://pytba.readthedocs.io/en/latest/
    botApp = telebot.TeleBot(
        token=TELEGRAM_TOKEN,
        threaded=False,
        state_storage=state_storage,
        use_class_middlewares=True,
    )

    # @see https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/step_example.py
    botApp.enable_save_next_step_handlers(delay=1)

    # XXX: This line causes an error:
    # AttributeError: partially initialized module 'botApp.botApp' has no attribute 'message_handler' (most likely due to a circular import)
    # Solution: Moved to `botCommands/commands.py`
    # botApp.load_next_step_handlers()

    # @see https://pytba.readthedocs.io/en/latest/sync_version/index.html#telebot.TeleBot.enable_saving_states
    # Default file name is `.state-save/states.pkl`
    botApp.enable_saving_states()

    # necessary for state parameter in handlers.
    from telebot.states.sync.middleware import StateMiddleware

    botApp.setup_middleware(StateMiddleware(botApp))
    botApp.add_custom_filter(custom_filters.StateFilter(botApp))

    return botApp


if not IS_TEST:
    botApp = startBotApp()


__all__ = [
    'botApp',
]
