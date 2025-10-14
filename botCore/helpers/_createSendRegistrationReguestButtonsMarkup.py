# -*- coding:utf-8 -*-

import telebot
from telebot import types

from core.constants import defaultLanguageCode  # pyTelegramBotAPI


def createSendRegistrationReguestButtonsMarkup(newUserId: int, newUserStr: str, languageCode: str | None):
    # @see https://core.telegram.org/bots/api#inlinekeyboardmarkup
    markup = types.InlineKeyboardMarkup(
        row_width=2,
    )
    # See https://core.telegram.org/bots/api#inlinekeyboardbutton
    str = newUserStr.replace(':', '-')
    castItem = types.InlineKeyboardButton(
        'Yes', callback_data=f'registerUser:{newUserId}:{str}:{languageCode or defaultLanguageCode}'
    )
    helpItem = types.InlineKeyboardButton('No', callback_data='cancel')
    markup.add(castItem, helpItem)
    return markup
