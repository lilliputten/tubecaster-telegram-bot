# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from botApp import botApp
from botCore import botConfig
from botCore.helpers import createCommonButtonsMarkup, getUserName
from core.appConfig import LOCAL, PROJECT_INFO, appConfig
from core.helpers.time import getTimeStamp
from core.logger import getDebugLogger, secondaryStyle, titleStyle
from core.utils import debugObj

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
        'Hi %s!' % name,
        'Welcome to the @TubeCasterBot!',
        'Use /cast to download an audio from the youtube video url, /info to get the video details, or just send me its url as a message.',
        'Also, /stats command will display your usage statistics, /status will show your usage plan and limits (if applicable), /plans will show details on available usage plans.',
        'Type /help to find all the available commands.',
        'Do not hesitate to reach the administrator (@lilliputten) in case of troubles.',
        'Take a look at the small reference at https://tubecaster.lilliputten.com/',
        'The bot version is %s.' % PROJECT_INFO,
    ]
    if LOCAL:
        msgItems.append(
            ' '.join(
                [
                    'ATTENTION: Sorry, but at the moment the bot is working in the LOCAL mode.',
                    "Probably, it won't be able to download any actual videos. Try a bit later please.",
                ]
            )
        )
    content = '\n\n'.join(filter(None, msgItems))
    _logger.info(logContent)
    # Show menu
    markup = createCommonButtonsMarkup()
    # Send content and menu with a banner
    with open(botConfig.visualImagePath, 'rb') as fh:
        botApp.send_photo(
            chatId,
            photo=fh,
            caption=content,
            reply_markup=markup,
            # parse_mode='Markdown',
        )
