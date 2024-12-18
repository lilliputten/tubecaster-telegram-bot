# -*- coding:utf-8 -*-

from flask import Response

from core.helpers.runtime import getModPath
from core.helpers.time import getTimeStamp
from core.logger import getLogger

from botApp import botApp

from .botRoutes import botRoutes

startTimeStr = getTimeStamp()

_logger = getLogger(getModPath())

logTraceback = False


@botRoutes.route('/stop')
def stopRoute():
    """
    Remove recent webhook from the telegram bot.
    """
    botApp.remove_webhook()
    botApp.stop_bot()
    _logger.info('stopRoute')
    return Response('The webhook has been deleted', headers={'Content-type': 'text/plain'})
