# -*- coding:utf-8 -*-

import time
import traceback
from flask import Blueprint
from flask import Response
from flask import request
import telebot

from core.logger import loggerConfig
from core.helpers.errors import errorToString
from core.helpers.time import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig, PROJECT_INFO
from core.utils import debugObj
from core.utils.generic import dictFromModule

from bot import botApp

from .commands import registerCommands
from . import botConfig

botRoutes = Blueprint('botRoutes', __name__)

startTimeStr = getTimeStamp(True)

_logger = getLogger('bot/botRoutes')

logTraceback = False


# Trace keys in logger and reponses
_debugKeysList = [
    'timeStr',
    'startTimeStr',
    'LOCAL',
    'WEBHOOK_URL',
]


def logBotStarted():
    """
    Debug: Show application start info.
    """
    content = '\n'.join(
        [
            'logBotStarted: botRoutes started',
            'Application: %s' % PROJECT_INFO,
        ]
    )
    _logger.info(content)


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
    timeStr = getTimeStamp(True)
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
    _logger.info('startRoute: Starting to register webhook:' + botConfig.WEBHOOK_URL)
    botApp.remove_webhook()
    time.sleep(1)
    return botApp.set_webhook(url=botConfig.WEBHOOK_URL)


@botRoutes.route('/')
def rootRoute():
    """
    Root page:
    Start telegram bot with the current webhook (deployed to vercel or local exposed with ngrok)
    """
    timeStr = getTimeStamp(True)
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
    timeStr = getTimeStamp(True)

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
    _logger.info('stopRoute')
    return Response('The webhook has been deleted', headers={'Content-type': 'text/plain'})


@botRoutes.route('/webhook', methods=['POST'])
def webhookRoute():
    """
    Process the telegram bot webhook.
    """
    timeStr = getTimeStamp(True)
    requestStream = request.stream.read().decode('utf-8')
    update = telebot.types.Update.de_json(requestStream)
    #  Sample update data: <telebot.types.Update object at 0x0000024A1904B5C0>
    #  chosen_inline_result = None
    #  deleted_business_messages = None
    #  edited_business_message = None
    #  edited_channel_post = None
    #  edited_message = None
    #  inline_query = None
    #  message = <telebot.types.Message object at 0x0000024A1904B560>
    #  message_reaction = None
    #  message_reaction_count = None
    #  my_chat_member = None
    #  poll = None
    #  poll_answer = None
    #  pre_checkout_query = None
    #  purchased_paid_media = None
    #  removed_chat_boost = None
    #  shipping_query = None
    #  update_id = 574259009
    obj = {
        **appConfig,
        **dictFromModule(botConfig),
        **{
            'startTimeStr': startTimeStr,
            'timeStr': timeStr,
            'update': type(update),
        },
    }
    logContent = '\n'.join(
        [
            'webhookRoute',
            debugObj(obj, _debugKeysList),
        ]
    )
    _logger.info(logContent)

    if update:
        try:
            botApp.process_new_updates([update])
        except Exception as err:
            sError = errorToString(err, show_stacktrace=False)
            sTraceback = str(traceback.format_exc())
            errMsg = 'webhookRoute: Error processing webhook update: ' + sError
            if logTraceback:
                errMsg += sTraceback
            else:
                _logger.info('webhookRoute: Traceback for the following error:' + sTraceback)
            _logger.error(errMsg)
            return Response(errMsg, headers={'Content-type': 'text/plain'})

    return Response('OK', headers={'Content-type': 'text/plain'})


# DEBUG
logBotStarted()


# Start commands
registerCommands()


# Module exports...
__all__ = [
    'botRoutes',
]
