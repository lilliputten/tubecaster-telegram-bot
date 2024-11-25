# -*- coding:utf-8 -*-

import telebot  # pytelegrambotapi
import re

from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig

from bot.botApp import botApp
from core.utils import debugObj

logger = getLogger('bot/commands/cast')

# Trace keys in logger and reponses
debugKeysList = [
    'url',
    'args',
    'timeStr',
    'chatId',
    'username',
    'LOCAL',
]


isYoutubeLink = re.compile(r'^https://\w*\.youtube.com/')

@botApp.message_handler(commands=['cast'])
def cast(message: telebot.types.Message):
    # Get core parameters
    text = message.text
    chat = message.chat
    chatId = chat.id
    username = chat.username
    # Parse text
    if not text:
        botApp.reply_to(message, 'Some arguments expected!')
        return
    args = text.strip().split()
    argsCount = len(args) - 1
    if argsCount < 1:
        botApp.reply_to(message, 'Too few arguments!')
        return
    elif argsCount > 1:
        botApp.reply_to(message, 'Too many arguments!')
        return
    url = args[1]
    if not isYoutubeLink.match(url):
        botApp.reply_to(message, 'The url should be a valid youtube link!')
        return
    # TODO: Do smth with the url
    obj = {
        **{
            'url': url,
            'args': ', '.join(args),
            'timeStr': getTimeStamp(True),
            'chatId': chatId,
            'username': username,
        },
        **appConfig,
    }
    debugData = debugObj(obj, debugKeysList)
    logContent = '\n\n'.join(
        [
            'command: %s' % text,
            debugData,
        ]
    )
    content = '\n\n'.join(
        [
            'Ok, your url is: %s' % url,
            debugData,
        ]
    )
    logger.info(logContent)
    botApp.send_message(chatId, content)
