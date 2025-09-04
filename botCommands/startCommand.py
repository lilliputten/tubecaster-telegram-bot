# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from botApp import botApp
from botCore import botConfig
from botCore.constants import emojies
from botCore.helpers import createCommonButtonsMarkup, getUserName
from core.appConfig import LOCAL, PROJECT_INFO, appConfig
from core.helpers.time import getTimeStamp
from core.logger import getDebugLogger, secondaryStyle, titleStyle
from core.utils import debugObj

_logger = getDebugLogger()


def startCommand(chat: telebot.types.Chat, message: telebot.types.Message):
    # userId = message.from_user.id if message.from_user else message.chat.id
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
        'Hi %s,' % name,
        'Welcome to the @TubeCasterBot!',
        'Do not hesitate to reach the administrator (@lilliputten) in case of troubles.',
        'Take a look at the brief application reference at https://tubecaster.lilliputten.com/',
        'The bot version is %s.' % PROJECT_INFO,
    ]
    content = '\n\n'.join(filter(None, msgItems))
    if len(content) > 1024:
        errStr = 'Message content is too long: ' + str(len(content))
        _logger.error(emojies.error + ' startCommand: ' + errStr)
    _logger.info(logContent)
    # Show menu
    markup = createCommonButtonsMarkup()
    # Send content and menu with a banner
    with open(botConfig.visualImagePath, 'rb') as fh:
        botApp.send_photo(
            chatId,
            photo=fh,
            caption=content,
            # parse_mode='Markdown',
        )
    # Prepare and send extra content (the limit for photo captions is 1024B)
    logContent = '\n'.join(logItems)
    msgItems = [
        'USAGE NOTES.',
        'Use /cast to download an audio from the youtube video url, /info to get the video details, or just send me its url as a message.',
        'Also, /stats command will display your usage statistics, /status will show your usage plan and limits (if applicable), /plans will show details on available usage plans.',
        'Type /help to find all the available commands.',
        'Please keep in mind that the bot is working in experimental mode and that Google may change its algorithms and API, which may lead to temporary disruptions in the application.',
        'Also keep in mind that downloading and processing audio files takes time and can take up to several minutes. If the bot has accepted your command for processing and it seems to you that the process has been delayed, please be patient. In case of long-term operations, the bot will send you notifications about the active process every minute.',
    ]
    if LOCAL:
        msgItems.append(
            ' '.join(
                [
                    'ATTENTION: The bot is working in a LOCAL mode.',
                    "Probably, it won't be able to download any actual videos. Try a bit later please.",
                ]
            )
        )
    # botApp.reply_to(msg
    botApp.send_message(
        chatId,
        emojies.info + ' ' + '\n\n'.join(filter(None, msgItems)),
        reply_markup=markup,
    )
