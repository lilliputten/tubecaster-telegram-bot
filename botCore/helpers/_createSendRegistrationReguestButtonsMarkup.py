# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI


def createSendRegistrationReguestButtonsMarkup(newUserId: int, newUserStr: str):
    # @see https://core.telegram.org/bots/api#inlinekeyboardmarkup
    markup = telebot.types.InlineKeyboardMarkup(
        row_width=2,
    )
    # See https://core.telegram.org/bots/api#inlinekeyboardbutton
    str = newUserStr.replace(':', '-')
    castItem = telebot.types.InlineKeyboardButton('Yes', callback_data=f'registerUser:{newUserId}:{str}')
    helpItem = telebot.types.InlineKeyboardButton('No', callback_data='cancel')
    markup.add(castItem, helpItem)
    return markup
