# -*- coding:utf-8 -*-

import time
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

from . import botCommands

from . import botConfig

startTimeStr = getTimeStamp(True)

logger = getLogger('bot/botBlueprint')

botBlueprint = Blueprint('botBlueprint', __name__)


# Trace keys in logger and reponses
debugKeysList = [
    'webhookUrl',
    # ...
    'startTimeStr',
    'timeStr',
    #  'changed',
    'LOCAL',
    # ...
    'WEBHOOK_HOST',
    'WEBHOOK_PATH',
    'TELEGRAM_TOKEN',
    'WERKZEUG_RUN_MAIN',
]


def logStart():
    """
    Debug: Show application start info.
    """
    obj = {
        **{
            'startTimeStr': startTimeStr,
            'timeStr': getTimeStamp(True),
        },
        **appConfig,
    }
    content = 'logStart:\n\n' + debugObj(obj, debugKeysList)
    logger.info(content)


@botBlueprint.route('/')
def root():
    obj = {
        **{
            'startTimeStr': startTimeStr,
            'timeStr': getTimeStamp(True),
        },
        **appConfig,
    }
    content = '\n\n'.join(
        [
            'root:',
            debugObj(obj, debugKeysList),
            'Use `/start` to start telegram bot',
        ]
    )
    return Response(content, headers={'Content-type': 'text/plain'})


@botBlueprint.route('/test')
def test():
    obj = {
        **{
            'startTimeStr': startTimeStr,
            'timeStr': getTimeStamp(True),
        },
        **appConfig,
    }
    content = '\n\n'.join(
        [
            'test:',
            debugObj(obj, debugKeysList),
        ]
    )
    logger.info(content)
    return Response(content, headers={'Content-type': 'text/plain'})


@botBlueprint.route('/start')
def start():
    botApp.remove_webhook()
    time.sleep(1)
    webhookUrl = botConfig.WEBHOOK_HOST + botConfig.WEBHOOK_PATH

    try:
        botApp.set_webhook(url=webhookUrl)
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        #  sTraceback = str(traceback.format_exc())
        errStr = 'Error registering web hook: ' + sError
        logger.error(errStr)
        return Response(errStr, headers={'Content-type': 'text/plain'})

    obj = {
        **{
            'webhookUrl': webhookUrl,
            'startTimeStr': startTimeStr,
            'timeStr': getTimeStamp(True),
        },
        **appConfig,
    }
    content = '\n\n'.join(
        [
            'start:',
            'The telegram bot has already set up for the webhook',
            debugObj(obj, debugKeysList),
        ]
    )
    logger.info(content)
    return Response(content, headers={'Content-type': 'text/plain'})


@botBlueprint.route('/webhook', methods=['POST'])
def webhook():
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
    requestStream = request.stream.read().decode('utf-8')
    update = telebot.types.Update.de_json(requestStream)
    obj = {
        **{
            'startTimeStr': startTimeStr,
            'timeStr': getTimeStamp(True),
            'update': str(update),
        },
        **appConfig,
    }
    content = '\n\n'.join(
        [
            'webhook:',
            debugObj(obj, debugKeysList),
        ]
    )
    logger.info(content)
    if update:
        botApp.process_new_updates([update])
    return Response('OK', headers={'Content-type': 'text/plain'})


# DEBUG
logStart()


# Module exports...
__all__ = [
    'botBlueprint',
]
