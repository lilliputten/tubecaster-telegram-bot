# -*- coding:utf-8 -*-

import time
import traceback
from flask import Blueprint
from flask import Response
from flask import request
import telebot

from core.helpers.errors import errorToString
from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig
from core.utils import debugObj
from core.utils.generic import dictFromModule

from bot.botApp import botApp

from .commands import registerCommands
from . import botConfig

botRoutes = Blueprint('botRoutes', __name__)

startTimeStr = getTimeStamp(True)

_logger = getLogger('bot/botRoutes')

_logTraceback = False


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
    content = '\n\n'.join(
        [
            'logBotStarted: botRoutes started',
        ]
    )
    _logger.info(content)


def getRemoteAddr():
    # request.remote_addr
    if 'X-Forwarded-For' in request.headers:
        proxy_data = request.headers['X-Forwarded-For']
        ip_list = proxy_data.split(',')
        return ip_list[0]  # first address in list is User IP
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']


@botRoutes.route('/test')
def testRoute():
    timeStr = getTimeStamp(True)
    # TODO: Dig into the vpn configuration to get the reason of absence of the real ip (looked for those `X-Forwarded` etc)
    #  remoteAddr = request.remote_addr # request.access_route # getAccessRoute()
    extraParams = {
        'timeStr': timeStr,
        'startTimeStr': startTimeStr,
        #  'remoteAddr': remoteAddr,
        #  'accessRoute': list(accessRoute),
        'headers': debugObj(dict(request.headers)),
        'environ': debugObj(dict(request.environ)),
        #  'requestDict': debugObj(request.__dict__),
    }
    obj = {
        **appConfig,
        **dictFromModule(botConfig),
        **extraParams,
    }
    keysList = _debugKeysList + list(extraParams.keys())
    titleStr = 'testRoute: Test @ %s' % timeStr
    logContent = '\n'.join(
        [
            titleStr,
            debugObj(obj, keysList),
        ]
    )
    content = '\n\n'.join(
        [
            titleStr,
            debugObj(obj, keysList),
        ]
    )
    _logger.info(logContent)
    return Response(content, headers={'Content-type': 'text/plain'})


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
                'Root route',
                #  debugStr,
            ]
        )
        _logger.info(logContent)
        #  raise Exception('Debugging error') # DEBUG
        return Response(content, headers={'Content-type': 'text/plain'})
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'rootRoute: Error processing route: ' + sError
        if _logTraceback:
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
        if _logTraceback:
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
            if _logTraceback:
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
