# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI


def getUserName(user: telebot.types.User | None):
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
    if not realName:
        realName = username
    if not realName:
        realName = '#' + str(userId)
    name = ' '.join(filter(None, [realName, '(@%s)' % username if username and realName != username else None]))
    return name
