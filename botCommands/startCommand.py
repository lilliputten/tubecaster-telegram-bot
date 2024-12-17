# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from core.helpers.time import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig, PROJECT_INFO
from core.utils import debugObj

from botApp import botApp
from botCore.helpers import createCommonButtonsMarkup

from botCore import botConfig


logger = getLogger('botCommands/startCommand')


def startCommand(chat: telebot.types.Chat):
    chatId = chat.id
    username = chat.username
    first_name = chat.first_name
    name = first_name if first_name else username
    obj = {
        'timeStr': getTimeStamp(),
        'chatId': chatId,
        'username': username,
        'first_name': first_name,
        'LOCAL': appConfig.get('LOCAL'),
    }
    logContent = '\n'.join(
        [
            'startCommand',
            debugObj(obj),
        ]
    )
    content = '\n\n'.join(
        [
            'Hi, %s!' % name,
            'Welcome to the TubeCaster bot!',
            'The bot version is: %s.' % PROJECT_INFO,
            'Use /cast to cast the youtube video to an audio. Type /help to find all commands.',
        ]
    )
    logger.info(logContent)
    # Show menu
    markup = createCommonButtonsMarkup()
    # Send content and menu with a banner
    with open(botConfig.visualImagePath, 'rb') as fh:
        botApp.send_photo(chatId, photo=fh, caption=content, reply_markup=markup)
