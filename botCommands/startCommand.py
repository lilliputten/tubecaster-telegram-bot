# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from core.helpers.time import getTimeStamp
from core.logger import getDebugLogger, titleStyle, secondaryStyle
from core.appConfig import LOCAL, appConfig, PROJECT_INFO
from core.utils import debugObj

from botApp import botApp
from botCore.helpers import createCommonButtonsMarkup, getUserName

from botCore import botConfig


_logger = getDebugLogger()


def startCommand(chat: telebot.types.Chat, message: telebot.types.Message):
    chatId = chat.id
    username = chat.username
    first_name = chat.first_name
    name = first_name if first_name else username
    debugItems = {
        'timeStr': getTimeStamp(),
        'chatId': chatId,
        'username': username,
        'usernameStr': getUserName(message.from_user),
        'first_name': first_name,
        'LOCAL': appConfig.get('LOCAL'),
    }
    logItems = [
        titleStyle('startCommand'),
        secondaryStyle(debugObj(debugItems)),
    ]
    logContent = '\n'.join(logItems)
    msgItems = [
        'Hi, %s!' % name,
        'Welcome to the TubeCaster bot!',
        'The bot version is: %s.' % PROJECT_INFO,
        'Use /cast to get an audio from the youtube video url or just send me its url as a message. Type /help to find all commands.',
        'Do not hesitate to reach the administrator (@lilliputten) in case of troubles.',
        ' '.join(
            [
                'ATTENTION: Sorry, but at the moment the bot works in the LOCAL mode!',
                " Probably, it won't be able to download any actual videos. Try a bit later please.",
            ]
        )
        if LOCAL
        else None,
    ]
    content = '\n\n'.join(filter(None, msgItems))
    _logger.info(logContent)
    # Show menu
    markup = createCommonButtonsMarkup()
    # Send content and menu with a banner
    with open(botConfig.visualImagePath, 'rb') as fh:
        botApp.send_photo(chatId, photo=fh, caption=content, reply_markup=markup)
