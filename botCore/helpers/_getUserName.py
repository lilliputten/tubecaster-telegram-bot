# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
from telebot import types


def getUserName(user: types.User | types.Chat | None, appendId: bool = False):
    if not user:
        return 'Unknown'
    userId = user.id if user else None
    username = user.username if user else None
    firstName = user.first_name if user else None
    lastName = user.last_name if user else None
    realNameList = [
        firstName,
        lastName,
    ]
    realName = ' '.join(filter(None, realNameList))
    extraItems = [
        '@' + username if username and realName else None,
        '#' + str(userId) if appendId and realName and username else None,
    ]
    if not realName:
        realName = '@' + username if username else '#' + str(userId)
    extra = ', '.join(filter(None, extraItems))
    name = ' '.join(filter(None, [realName, f'({extra})' if extra else None]))
    return name
