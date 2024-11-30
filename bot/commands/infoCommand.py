# -*- coding:utf-8 -*-

import telebot  # pytelegrambotapi

from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig

from bot.botApp import botApp
from core.utils import debugObj


_logger = getLogger('bot/commands/infoCommand')


@botApp.message_handler(commands=['info'])
def infoCommand(message: telebot.types.Message):
    text = message.text
    chat = message.chat
    chatId = chat.id
    username = chat.username
    first_name = chat.first_name
    last_name = chat.last_name
    #  name = first_name if first_name else username
    obj = {
        'timeStr': getTimeStamp(True),
        'chatId': chatId,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'LOCAL': appConfig.get('LOCAL'),
    }
    logContent = '\n'.join(
        [
            'infoCommand: %s' % text,
            debugObj(obj),
        ]
    )
    content = '\n\n'.join(
        [
            'infoCommand: %s' % text,
        ]
    )
    _logger.info(logContent)
    botApp.send_message(chatId, content)
