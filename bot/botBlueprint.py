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

logger = getLogger('bot/botBlueprint')

botBlueprint = Blueprint('botBlueprint', __name__)


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
            'logBotStarted @ %s' % timeStr,
            debugObj(obj, debugKeysList),
        ]
    )
    logger.info(content)


@botBlueprint.route('/test')
def test():
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
            'route: test @ %s' % timeStr,
            debugObj(obj, debugKeysList),
        ]
    )
    logger.info(content)
    return Response(content, headers={'Content-type': 'text/plain'})


def initWebhook():
    botApp.remove_webhook()
    time.sleep(1)
    return botApp.set_webhook(url=botConfig.WEBHOOK_URL)


@botBlueprint.route('/')
def init():
    """
    Root page:
    Start telegram bot with the current webhook (deployed to vercel or local exposed with ngrok)
    """
    timeStr = getTimeStamp(True)

    try:
        initWebhook()
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errStr = 'route: start: Error registering web hook: ' + sError
        logger.error(errStr)
        return Response(errStr, headers={'Content-type': 'text/plain'})

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
            'route: init @ %s' % timeStr,
            debugData,
            'Use `/start` to start telegram bot',
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


@botBlueprint.route('/stop')
def stop():
    """
    Remove recent webhook from the telegram bot.
    """
    botApp.remove_webhook()
    logger.info('route: stop')
    return Response('The webhook has been deleted', headers={'Content-type': 'text/plain'})


@botBlueprint.route('/webhook', methods=['POST'])
def webhook():
    """
    Process the telegram bot webhook.
    """
    timeStr = getTimeStamp(True)
    logger.info('route: webhook start %s' % timeStr)
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
            'route: webhook %s info' % timeStr,
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
            errStr = 'route: webhook: Error processing webhook update: ' + sError
            logger.error(errStr)
            print(sTraceback)
            return Response(errStr, headers={'Content-type': 'text/plain'})

    return Response('OK', headers={'Content-type': 'text/plain'})


# DEBUG
logBotStarted()

# Start commands
registerCommands()

# Module exports...
__all__ = [
    'botBlueprint',
]
