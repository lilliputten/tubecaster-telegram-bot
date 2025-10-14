# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
from telebot import types

from botApp import botApp
from botCore import botConfig

from .commandsInfo import commandsInfo

#  _logger = getDebugLogger()


def helpCommand(chat: types.Chat):
    chatId = chat.id
    helpText = 'The following commands are available: \n\n'
    for key in commandsInfo:
        helpText += '/' + key + ': '
        helpText += commandsInfo[key] + '\n'
    # Send content and menu with a banner
    with open(botConfig.coverImagePath, 'rb') as fh:
        botApp.send_photo(
            chatId,
            photo=fh,
            caption=helpText,
            reply_markup=types.ReplyKeyboardRemove(),
        )
