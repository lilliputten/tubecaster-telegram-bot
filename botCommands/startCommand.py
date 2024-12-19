# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from core.helpers.time import getTimeStamp
from core.logger import getDebugLogger
from core.appConfig import LOCAL, appConfig, PROJECT_INFO
from core.utils import debugObj

from botApp import botApp
from botCore.helpers import createCommonButtonsMarkup

from botCore import botConfig


logger = getDebugLogger()


def startCommand(chat: telebot.types.Chat):
    chatId = chat.id
    username = chat.username
    first_name = chat.first_name
    name = first_name if first_name else username
    debugItems = {
        'timeStr': getTimeStamp(),
        'chatId': chatId,
        'username': username,
        # 'usernameStr': getUserName(user),
        'first_name': first_name,
        'LOCAL': appConfig.get('LOCAL'),
    }
    logItems = [
        'startCommand',
        debugObj(debugItems),
    ]
    logContent = '\n'.join(logItems)
    msgItems = [
        'Hi, %s!' % name,
        'Welcome to the TubeCaster bot!',
        'The bot version is: %s.' % PROJECT_INFO,
        'Use /cast to cast the youtube video to an audio. Type /help to find all commands.',
        ' '.join(
            [
                'ATTENTION: Sorry, but at the moment the bot works in the LOCAL mode!',
                " Probably, it won't be able to download any actual videos. Try a bit later please.",
            ]
        )
        if LOCAL
        else None,
    ]
    content = '\n\n'.join(msgItems)
    logger.info(logContent)
    # Show menu
    markup = createCommonButtonsMarkup()
    # Send content and menu with a banner
    with open(botConfig.visualImagePath, 'rb') as fh:
        botApp.send_photo(chatId, photo=fh, caption=content, reply_markup=markup)
