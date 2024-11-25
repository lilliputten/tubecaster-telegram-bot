# -*- coding:utf-8 -*-

import telebot  # pytelegrambotapi

from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig

from bot.botApp import botApp
from core.utils import debugObj

logger = getLogger('bot/commands/start')

# Trace keys in logger and reponses
debugKeysList = [
    'timeStr',
    'chatId',
    'username',
    'first_name',
    'last_name',
    'language_code',
    'LOCAL',
]


@botApp.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = message.text
    chat = message.chat
    chatId = chat.id
    username = chat.username
    first_name = chat.first_name
    last_name = chat.last_name
    name = first_name if first_name else username
    obj = {
        **{
            'timeStr': getTimeStamp(True),
            'chatId': chatId,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
        },
        **appConfig,
    }
    logContent = '\n\n'.join(
        [
            'command: %s' % text,
            debugObj(obj, debugKeysList),
        ]
    )
    content = '\n\n'.join(
        [
            'Hi, %s!' % name,
            'Welcome to the TubeCaster bot!',
            'Type /help to find all commands.',
        ]
    )
    logger.info(logContent)
    botApp.send_message(chatId, content)
