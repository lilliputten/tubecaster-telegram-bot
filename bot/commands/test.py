# -*- coding:utf-8 -*-

import telebot  # pytelegrambotapi

#  from core.helpers.errors import errorToString
from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig

from bot.botApp import botApp
from core.utils import debugObj

#  from . import botConfig

logger = getLogger('bot/commands/test')

# Trace keys in logger and reponses
debugKeysList = [
    'timeStr',
    'chatId',
    'username',
    'first_name',
    'LOCAL',
]


@botApp.message_handler(commands=['test'])
def test(message: telebot.types.Message):
    chat = message.chat
    chatId = chat.id
    username = chat.username
    first_name = chat.first_name
    name = first_name if first_name else username
    #  json = message.json
    obj = {
        **{
            'timeStr': getTimeStamp(True),
            'chatId': chatId,
            'username': username,
            'first_name': first_name,
        },
        **appConfig,
    }
    logContent = '\n\n'.join(
        [
            'test command:',
            debugObj(obj, debugKeysList),
        ]
    )
    content = '\n\n'.join(
        [
            'Hi %s! Welcome to the TubeCaster bot!' % name,
            debugObj(obj, debugKeysList),
            'Type /help to find all commands.',
        ]
    )
    logger.info(logContent)
    botApp.send_message(chatId, content)
