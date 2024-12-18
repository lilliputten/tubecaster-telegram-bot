# -*- coding:utf-8 -*-

import time
import traceback
from flask import Response
from flask import request

from core.appConfig import appConfig, PROJECT_INFO
from core.helpers.errors import errorToString
from core.helpers.runtime import getModPath
from core.helpers.time import getTimeStamp
from core.logger import getLogger, loggerConfig
from core.utils import debugObj
from core.utils.generic import dictFromModule

from botApp import botApp
from botCore import botConfig
from botCore.botConfig import WEBHOOK_URL

from .botRoutes import botRoutes

startTimeStr = getTimeStamp()

_logger = getLogger(getModPath())

logTraceback = False


# Trace keys in logger and reponses
_debugKeysList = [
    'timeStr',
    'startTimeStr',
    'LOCAL',
    'WEBHOOK_URL',
]


def getRemoteAddr():
    """
    NOTE: It's not possible to get the remote address on the VDS server under VLESS proxy (TODO?)
    """
    # request.remote_addr
    if 'X-Forwarded-For' in request.headers:
        proxy_data = request.headers['X-Forwarded-For']
        ip_list = proxy_data.split(',')
        return ip_list[0]  # first address in list is User IP
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']


def truncStr(str: str, maxLen: int):
    if len(str) >= maxLen - 3:
        str = str[: maxLen - 3] + '...'
    return str


@botRoutes.route('/test')
def testRoute():
    """
    Get the deep debugging info
    """
    timeStr = getTimeStamp()
    try:
        extraParams = {
            'timeStr': timeStr,
            'startTimeStr': startTimeStr,
            #  'headers': debugObj(dict(request.headers)),
            #  'environ': debugObj(dict(request.environ)),
            'PROJECT_INFO': PROJECT_INFO,
            #  'requestDict': debugObj(request.__dict__),
            'LOGS_SERVER_HOST': appConfig.get('LOGS_SERVER_HOST'),
            'LOGS_SERVER_URL': loggerConfig.LOGS_SERVER_URL,
            'LOGS_SERVER_PORT': appConfig.get('LOGS_SERVER_PORT'),
            'YT_COOKIE': truncStr(appConfig.get('YT_COOKIE', 'NONE'), 50),
        }
        obj = {
            **appConfig,
            **dictFromModule(botConfig),
            **extraParams,
        }
        keysList = _debugKeysList + list(extraParams.keys())
        titleStr = 'testRoute: Test @ %s' % timeStr
        debugStr = debugObj(obj, keysList)
        logContent = '\n'.join(
            [
                titleStr,
                debugStr,
            ]
        )
        content = '\n\n'.join(
            [
                titleStr,
                debugStr,
            ]
        )
        _logger.info(logContent)
        #  raise Exception('Debugging error') # DEBUG
        return Response(content, headers={'Content-type': 'text/plain'})
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'testRoute: Error processing test route: ' + sError
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('testRoute: Traceback for the following error:' + sTraceback)
        _logger.error(errMsg)
        return Response(errMsg, headers={'Content-type': 'text/plain'})


# Real code start...


def initWebhook():
    _logger.info('initWebhook: Starting to register webhook:' + WEBHOOK_URL)
    botApp.remove_webhook()
    time.sleep(1)
    # @see https://pytba.readthedocs.io/en/latest/sync_version/index.html#telebot.TeleBot.set_webhook
    return botApp.set_webhook(
        url=WEBHOOK_URL,
        timeout=600,  # Increase timeout to allow long video downloads
    )


@botRoutes.route('/')
def rootRoute():
    """
    Root page:
    Start telegram bot with the current webhook (deployed to vercel or local exposed with ngrok)
    """
    timeStr = getTimeStamp()
    try:
        obj = {
            **appConfig,
            **dictFromModule(botConfig),
            **{
                'timeStr': timeStr,
                'startTimeStr': startTimeStr,
            },
        }
        debugStr = debugObj(obj, _debugKeysList)
        logContent = '\n'.join(
            [
                'rootRoute: Empty test route',
                debugStr,
            ]
        )
        content = '\n\n'.join(
            [
                #  'Root route',
                'Application: %s' % PROJECT_INFO,
                #  debugStr,
            ]
        )
        _logger.info(logContent)
        #  raise Exception('Debugging error') # DEBUG
        return Response(content, headers={'Content-type': 'text/plain'})
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'rootRoute: Error processing root route: ' + sError
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('rootRoute: Traceback for the following error:' + sTraceback)
        _logger.error(errMsg)
        return Response(errMsg, headers={'Content-type': 'text/plain'})


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

    obj = {
        **appConfig,
        **dictFromModule(botConfig),
        **{
            'startTimeStr': startTimeStr,
            'timeStr': timeStr,
        },
    }
    debugStr = debugObj(obj, _debugKeysList)
    logContent = '\n'.join(
        [
            'startRoute: Webhook adding result: %s' % 'Succeed' if result else 'Failed',
            debugStr,
        ]
    )
    content = '\n\n'.join(
        [
            'Webhook has been already initialized' if result else 'Webhook initalisation failed',
            'Application: %s' % PROJECT_INFO,
            #  debugStr,
        ]
    )
    _logger.info(logContent)
    return Response(content, headers={'Content-type': 'text/plain'})


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
