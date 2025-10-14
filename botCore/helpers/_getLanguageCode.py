# -*- coding:utf-8 -*-

import telebot
from telebot import types

from core.constants import defaultLanguageCode  # pyTelegramBotAPI


def getLanguageCode(message: types.Message):
    json = message.json
    json = json.get('reply_to_message', json)
    fromData: dict = json.get('from', {})
    languageCode = str(fromData.get('language_code', defaultLanguageCode))
    return languageCode
