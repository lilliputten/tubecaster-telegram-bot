# -*- coding:utf-8 -*-

from datetime import datetime

import telebot  # pyTelegramBotAPI
from dateutil.relativedelta import relativedelta

from botApp import botApp
from botCore.constants import emojies
from botCore.helpers import createRemoveAccountButtonsMarkup, getUserName
from core.appConfig import LOCAL, PROJECT_INFO, appConfig
from core.helpers.time import formatTime, getTimeStamp
from core.logger import getDebugLogger, secondaryStyle, titleStyle
from core.utils import debugObj
from db import findUser

_logger = getDebugLogger()


def showRemoveAccountDialog(message: telebot.types.Message):
    chat = message.chat
    chatId = chat.id
    username = chat.username
    first_name = chat.first_name
    # name = first_name if first_name else username
    userId = message.from_user.id if message.from_user else message.chat.id
    user = findUser({'id': userId})   # , 'isDeleted': False})
    if not user:
        botApp.reply_to(
            message,
            emojies.error + ' You do not have an account here yet. So, you do not need to wipe it.',
        )
        return
    if user.isDeleted:
        deletedAt = user.deletedAt or datetime.now()
        willBeDeletedAt = deletedAt + relativedelta(months=+1)
        botApp.reply_to(
            message,
            emojies.error
            + f' Your account has been already marked to deletion on {formatTime("onlyDate", deletedAt)} (and will be wiped out on {formatTime("onlyDate", willBeDeletedAt)}). You can restore the account via /restore_account command.',
        )
        return
    debugItems = {
        'timeStr': getTimeStamp(),
        'userId': userId,
        'chatId': chatId,
        'username': username,
        'usernameStr': getUserName(message.from_user),
        'first_name': first_name,
        'LOCAL': appConfig.get('LOCAL'),
    }
    logItems = [
        titleStyle('showRemoveAccountDialog'),
        secondaryStyle(debugObj(debugItems)),
    ]
    logContent = '\n'.join(logItems)
    msgItems = [
        'Are you sure you want to remove your account?',
    ]
    content = '\n\n'.join(filter(None, msgItems))
    _logger.info(logContent)
    # Show menu
    markup = createRemoveAccountButtonsMarkup()
    # Send content and menu with a banner
    botApp.reply_to(
        message,
        emojies.question + ' ' + content,
        reply_markup=markup,
    )
