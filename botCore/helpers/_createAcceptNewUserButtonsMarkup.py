# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI


def createAcceptNewUserButtonsMarkup(newUserId: int, newUserStr: str):
    # @see https://core.telegram.org/bots/api#inlinekeyboardmarkup
    markup = telebot.types.InlineKeyboardMarkup(
        row_width=2,
    )
    # See https://core.telegram.org/bots/api#inlinekeyboardbutton
    str = newUserStr.replace(':', '-')
    castItem = telebot.types.InlineKeyboardButton('Accept', callback_data=f'acceptUser:{newUserId}:{str}')
    helpItem = telebot.types.InlineKeyboardButton('Refuse', callback_data=f'refuseUser:{newUserId}:{str}')
    markup.add(castItem, helpItem)
    return markup
