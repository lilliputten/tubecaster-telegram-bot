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

from bot.botApp import botApp
from core.utils import debugObj
from core.utils.generic import dictFromModule

from .commands import registerCommands
from . import botConfig

startTimeStr = getTimeStamp(True)

logger = getLogger('bot/botRoutes')

botRoutes = Blueprint('botRoutes', __name__)

logTraceback = False


# Trace keys in logger and reponses
debugKeysList = [
    'startTimeStr',
    'timeStr',
    'LOCAL',
    'WEBHOOK_URL',
]


def logBotStarted():
    """
    Debug: Show application start info.
    """
    #  timeStr = getTimeStamp(True)
    #  obj = {
    #      **appConfig,
    #      **dictFromModule(botConfig),
    #      **{
    #          'startTimeStr': startTimeStr,
    #          'timeStr': timeStr,
    #      },
    #  }
    content = '\n\n'.join(
        [
            'logBotStarted: botRoutes started',
            #  debugObj(obj, debugKeysList),
        ]
    )
    logger.info(content)


@botRoutes.route('/test')
def testRoute():
    timeStr = getTimeStamp(True)
    obj = {
        **appConfig,
        **dictFromModule(botConfig),
        **{
            'startTimeStr': startTimeStr,
            'timeStr': timeStr,
        },
    }
    content = '\n\n'.join(
        [
            'testRoute @ %s' % timeStr,
            debugObj(obj, debugKeysList),
        ]
    )
    logger.info(content)
    return Response(content, headers={'Content-type': 'text/plain'})


def initWebhook():
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
    obj = {
        **appConfig,
        **dictFromModule(botConfig),
        **{
            'startTimeStr': startTimeStr,
            'timeStr': timeStr,
        },
    }
    debugData = debugObj(obj, debugKeysList)
    logContent = '\n\n'.join(
        [
            'rootRoute: Empty test route',
            debugData,
        ]
    )
    content = '\n\n'.join(
        [
            'The webhook has been already initialized with url "%s".' % botConfig.WEBHOOK_URL,
            debugData,
        ]
    )
    logger.info(logContent)
    return Response(content, headers={'Content-type': 'text/plain'})


@botRoutes.route('/')
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
            logger.info('startRoute: Traceback for the following error:' + sTraceback)
        logger.error(errMsg)
        return Response(errMsg, headers={'Content-type': 'text/plain'})

    obj = {
        **appConfig,
        **dictFromModule(botConfig),
        **{
            'startTimeStr': startTimeStr,
            'timeStr': timeStr,
        },
    }
    debugData = debugObj(obj, debugKeysList)
    logContent = '\n\n'.join(
        [
            'startRoute: Webhook adding result: %s' % 'Succeed' if result else 'Failed',
            debugData,
        ]
    )
    content = '\n\n'.join(
        [
            'The webhook has been already initialized with url "%s".' % botConfig.WEBHOOK_URL,
            debugData,
        ]
    )
    logger.info(logContent)
    return Response(content, headers={'Content-type': 'text/plain'})


@botRoutes.route('/stop')
def stopRoute():
    """
    Remove recent webhook from the telegram bot.
    """
    botApp.remove_webhook()
    logger.info('stopRoute')
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
    content = '\n\n'.join(
        [
            'webhookRoute',
            debugObj(obj, debugKeysList),
        ]
    )
    logger.info(content)

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
                logger.info('webhookRoute: Traceback for the following error:' + sTraceback)
            logger.error(errMsg)
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
