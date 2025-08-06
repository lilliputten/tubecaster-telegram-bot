# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI


def createCommonButtonsMarkup():
    # @see https://core.telegram.org/bots/api#inlinekeyboardmarkup
    markup = telebot.types.InlineKeyboardMarkup(
        row_width=2,
    )
    # See https://core.telegram.org/bots/api#inlinekeyboardbutton
    castItem = telebot.types.InlineKeyboardButton('Get audio', callback_data='startCast')
    helpItem = telebot.types.InlineKeyboardButton('Show help', callback_data='startHelp')
    markup.add(castItem, helpItem)
    return markup
