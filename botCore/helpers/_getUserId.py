# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
from telebot import types


def getUserId(message: types.Message):
    userId = message.from_user.id if message.from_user else message.chat.id
    return userId
