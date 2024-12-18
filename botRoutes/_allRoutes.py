# -*- coding:utf-8 -*-

import time
import traceback
from flask import Response
from flask import request

from core.appConfig import appConfig, PROJECT_INFO
from core.helpers.errors import errorToString

from core.helpers.time import getTimeStamp
from core.logger import getDebugLogger, loggerConfig
from core.utils import debugObj
from core.utils.generic import dictFromModule

from botApp import botApp
from botCore import botConfig
from botCore.botConfig import WEBHOOK_URL

from .botRoutes import botRoutes

startTimeStr = getTimeStamp()

_logger = getDebugLogger()

logTraceback = False


# Real code start...


@botRoutes.route('/stop')
def stopRoute():
    """
    Remove recent webhook from the telegram bot.
    """
    botApp.remove_webhook()
    botApp.stop_bot()
    _logger.info('stopRoute')
    return Response('The webhook has been deleted', headers={'Content-type': 'text/plain'})


# Module exports...
__all__ = []
