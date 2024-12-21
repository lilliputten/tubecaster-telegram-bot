# -*- coding:utf-8 -*-

from functools import partial
import telebot  # pyTelegramBotAPI

from botCore.helpers import getUserName
from core.helpers.urls import isYoutubeLink
from core.logger import getDebugLogger
from core.utils import debugObj

from botApp import botApp
from botCore.constants import emojies
from botCore.helpers import replyOrSend
from botCast import downloadAndSendAudioToChat


_logger = getDebugLogger()


def castForUrlStep(chat: telebot.types.Chat, message: telebot.types.Message):
    text = message.text
    chatId = chat.id
    username = getUserName(message.from_user)
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
            'castForUrlStep: Start',
            debugStr,
        ]
    )
    _logger.info(logContent)
    downloadAndSendAudioToChat(url, chatId, username, message)


def castCommand(chat: telebot.types.Chat, message: telebot.types.Message):
    """
    Expects commands like:
    `/cast URL`
    or just
    `URL`
    """
    chatId = chat.id
    username = getUserName(message.from_user)
    text = message.text if message and message.text else ''
    args = text.strip().split()
    argsCount = len(args) - 1
    if argsCount < 1:
        if not args[0] or not isYoutubeLink(args[0]):
            replyMsg = emojies.success + ' Ok, now send the video address:'
            replyOrSend(botApp, replyMsg, chat.id, message)
            botApp.register_next_step_handler(message, partial(castForUrlStep, chat))
            return
        # Else continue with th first argument as an url
    elif argsCount > 1:
        botApp.reply_to(message, 'Too many arguments (expected only video address).')
        return
    # Get the last argument
    url = args[argsCount - 1]
    downloadAndSendAudioToChat(url, chatId, username, message)
