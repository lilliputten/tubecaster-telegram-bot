# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
from telebot import types


def createRemoveAccountButtonsMarkup():
    # @see https://core.telegram.org/bots/api#inlinekeyboardmarkup
    markup = types.InlineKeyboardMarkup(
        row_width=2,
    )
    # See https://core.telegram.org/bots/api#inlinekeyboardbutton
    yes = types.InlineKeyboardButton('Yes', callback_data='removeAccountYes')
    no = types.InlineKeyboardButton('No', callback_data='removeAccountNo')
    markup.add(yes, no)
    return markup
