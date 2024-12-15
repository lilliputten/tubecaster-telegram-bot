# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
from functools import partial

from core.helpers.time import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig
from bot.botApp import botApp
from core.utils import debugObj

from bot.cast import replyOrSend
from bot.cast import sendInfoToChat

_logger = getLogger('bot/commands/infoCommand')


def infoForUrlStep(chat: telebot.types.Chat, message: telebot.types.Message):
    text = message.text
    chatId = chat.id
    username = str(chat.username)
    if not text:
        botApp.reply_to(message, 'Video url is expected.')
        return
    url = text
    obj = {
        'url': url,
        'chatId': chatId,
        'username': username,
    }
    debugStr = debugObj(obj)
    logContent = '\n'.join(
        [
            'infoForUrlStep: Start',
            debugStr,
        ]
    )
    _logger.info(logContent)
    sendInfoToChat(url, chat, message)


def infoCommand(chat: telebot.types.Chat, message: telebot.types.Message):
    text = message.text if message and message.text else ''
    args = text.strip().split()
    argsCount = len(args) - 1
    if argsCount < 1:
        replyMsg = 'Ok, now send the video address:'
        replyOrSend(replyMsg, chat, message)
        botApp.register_next_step_handler(message, partial(infoForUrlStep, chat))
        return
    elif argsCount > 1:
        botApp.reply_to(message, 'Too many arguments (expected only video address).')
        return
    url = args[1]
    sendInfoToChat(url, chat, message)
