# -*- coding:utf-8 -*-

import time
import traceback
from flask import Response

from core.appConfig import PROJECT_INFO
from core.helpers.errors import errorToString
from core.helpers.runtime import getModPath
from core.helpers.time import getTimeStamp
from core.logger import getLogger
from core.utils import debugObj

from botApp import botApp
from botCore.botConfig import WEBHOOK_URL

from .botRoutes import botRoutes

startTimeStr = getTimeStamp()

_logger = getLogger(getModPath())

logTraceback = False


def initWebhook():
    _logger.info('initWebhook: Starting to register webhook:' + WEBHOOK_URL)
    botApp.remove_webhook()
    time.sleep(1)
    # @see https://pytba.readthedocs.io/en/latest/sync_version/index.html#telebot.TeleBot.set_webhook
    return botApp.set_webhook(
        url=WEBHOOK_URL,
        timeout=600,  # Increase timeout to allow long video downloads
    )


@botRoutes.route('/start')
def startRoute():
    """
    Root page:
    Start telegram bot with the current webhook (deployed to vercel or local exposed with ngrok)
    """
    timeStr = getTimeStamp()

    result: bool
    try:
        result = initWebhook()
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'startRoute: Error registering webhook: ' + sError
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('startRoute: Traceback for the following error:' + sTraceback)
        _logger.error(errMsg)
        return Response(errMsg, headers={'Content-type': 'text/plain'})

    debugItems = {
        'startTimeStr': startTimeStr,
        'timeStr': timeStr,
    }
    debugStr = debugObj(debugItems)
    logItems = [
        'startRoute: Webhook adding result: %s' % 'Succeed' if result else 'Failed',
        debugStr,
    ]
    logContent = '\n'.join(logItems)
    msgItems = [
        'Webhook has been already initialized' if result else 'Webhook initalisation failed',
        'Application: %s' % PROJECT_INFO,
        #  debugStr,
    ]
    msgContent = '\n\n'.join(msgItems)
    _logger.info(logContent)
    return Response(msgContent, headers={'Content-type': 'text/plain'})
