# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI


def getUserId(message: telebot.types.Message):
    userId = message.from_user.id if message.from_user else message.chat.id
    return userId
