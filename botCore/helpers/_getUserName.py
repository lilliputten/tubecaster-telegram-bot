# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI


def getUserName(user: telebot.types.User | None):
    if not user:
        return None
    userId = user.id if user else None
    username = user.username if user else None
    firstName = user.first_name if user else None
    lastName = user.last_name if user else None
    realName = ' '.join(
        filter(
            None,
            [
                firstName,
                lastName,
            ],
        )
    )
    if not realName:
        realName = username
    if not realName:
        realName = '#' + str(userId)
    name = ' '.join(filter(None, [realName, '(%s)' % username if username and realName != username else None]))
    return name
