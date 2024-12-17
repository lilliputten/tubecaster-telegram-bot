# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from botApp import botApp

from .. import botConfig

from .commandsInfo import commandsInfo


#  _logger = getLogger('bot/commands/helpCommand')


def helpCommand(chat: telebot.types.Chat):
    chatId = chat.id
    helpText = 'The following commands are available: \n\n'
    for key in commandsInfo:
        helpText += '/' + key + ': '
        helpText += commandsInfo[key] + '\n'
    # Send content and menu with a banner
    with open(botConfig.coverImagePath, 'rb') as fh:
        botApp.send_photo(chatId, photo=fh, caption=helpText)
