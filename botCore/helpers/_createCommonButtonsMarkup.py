# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
from telebot import types


def createCommonButtonsMarkup():
    # @see https://core.telegram.org/bots/api#inlinekeyboardmarkup
    markup = types.InlineKeyboardMarkup(
        row_width=2,
    )
    # See https://core.telegram.org/bots/api#inlinekeyboardbutton
    castItem = types.InlineKeyboardButton('Get audio', callback_data='startCast')
    helpItem = types.InlineKeyboardButton('Show help', callback_data='startHelp')
    markup.add(castItem, helpItem)
    return markup
