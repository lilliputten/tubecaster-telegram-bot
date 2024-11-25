# -*- coding:utf-8 -*-

import telebot  # pytelegrambotapi
import traceback

#  from core.helpers.errors import errorToString
from core.helpers.errors import errorToString
from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig

from bot.botApp import botApp
from core.utils import debugObj

#  from . import botConfig

logger = getLogger('bot/commands/test')

# Trace keys in logger and reponses
debugKeysList = [
    'text',
    'timeStr',
    'chatId',
    'username',
    'first_name',
    'last_name',
    'language_code',
    'LOCAL',
]


@botApp.message_handler(commands=['test'])
def testCommand(message: telebot.types.Message):
    try:
        text = message.text
        chat = message.chat
        chatId = chat.id
        username = chat.username
        first_name = chat.first_name
        last_name = chat.last_name
        name = first_name if first_name else username
        json = message.json
        language_code = json.get('from', {}).get('language_code')
        obj = {
            **{
                'text': text,
                'timeStr': getTimeStamp(True),
                'chatId': chatId,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'language_code': language_code,
            },
            **appConfig,
        }
        logContent = '\n\n'.join(
            [
                'testCommand',
                debugObj(obj, debugKeysList),
            ]
        )
        content = '\n\n'.join(
            [
                'Hi, %s! Here is your test results:' % name,
                debugObj(obj, debugKeysList),
            ]
        )
        logger.info(logContent)
        botApp.send_message(chatId, content)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'Error: ' + errText
        logger.error('testCommand: ' + errMsg)
        print(sTraceback)
        botApp.reply_to(message, errMsg)
