# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI


def createRemoveAccountButtonsMarkup():
    # @see https://core.telegram.org/bots/api#inlinekeyboardmarkup
    markup = telebot.types.InlineKeyboardMarkup(
        row_width=2,
    )
    # See https://core.telegram.org/bots/api#inlinekeyboardbutton
    yes = telebot.types.InlineKeyboardButton('Yes', callback_data='removeAccountYes')
    no = telebot.types.InlineKeyboardButton('No', callback_data='removeAccountNo')
    markup.add(yes, no)
    return markup
