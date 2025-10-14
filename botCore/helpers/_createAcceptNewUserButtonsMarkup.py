# -*- coding:utf-8 -*-

import telebot
from telebot import types

from core.constants import defaultLanguageCode  # pyTelegramBotAPI


def createAcceptNewUserButtonsMarkup(newUserId: int, newUserStr: str, languageCode: str | None):
    # @see https://core.telegram.org/bots/api#inlinekeyboardmarkup
    markup = types.InlineKeyboardMarkup(
        row_width=2,
    )
    # See https://core.telegram.org/bots/api#inlinekeyboardbutton
    str = newUserStr.replace(':', '-')
    if not languageCode:
        languageCode = defaultLanguageCode  # 'en'
    castItem = types.InlineKeyboardButton('Accept', callback_data=f'acceptUser:{newUserId}:{str}:{languageCode}')
    helpItem = types.InlineKeyboardButton('Refuse', callback_data=f'rejectUser:{newUserId}:{str}:{languageCode}')
    markup.add(castItem, helpItem)
    return markup
