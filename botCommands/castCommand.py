# -*- coding:utf-8 -*-

from functools import partial
import telebot  # pyTelegramBotAPI
from telebot.states.sync.context import StateContext

from core.helpers.urls import isYoutubeLink
from core.logger import getDebugLogger, titleStyle, secondaryStyle
from core.utils import debugObj

from botApp import botApp
from botApp.botStates import BotStates
from botCore.helpers import getUserName
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
    if not isYoutubeLink(url):
        botApp.reply_to(
            message,
            emojies.error + ' A youtube url has been expected to fetch a video from. But you\'ve sent "%s".' % url,
        )
        return
    obj = {
        'url': url,
        'chatId': chatId,
        'username': username,
    }
    debugStr = debugObj(obj)
    logItems = [
        titleStyle('castForUrlStep: Start'),
        secondaryStyle(debugStr),
    ]
    logContent = '\n'.join(logItems)
    _logger.info(logContent)
    downloadAndSendAudioToChat(url, chatId, username, message)


def startWaitingForCastUrl(
    chat: telebot.types.Chat,
    message: telebot.types.Message,
):
    chatId = chat.id
    userId = message.from_user.id if message.from_user else chatId
    replyMsg = emojies.question + ' Ok, now send the video address:'
    replyOrSend(botApp, replyMsg, chat.id, message)
    _logger.info('startWaitingForCastUrl: Setting state to waitForCastUrl')
    # NOTE: Next step doesn't work on vds deployed server for a reason, using state (see below)
    botApp.register_next_step_handler(message, partial(castForUrlStep, chat))
    # state.set(BotStates.waitForCastUrl)
    botApp.set_state(userId, BotStates.waitForCastUrl)


def castCommand(
    chat: telebot.types.Chat,
    message: telebot.types.Message,
    state: StateContext,
):
    """
    Expects commands like:
    `/cast URL`
    or just
    `URL`
    """
    chatId = chat.id
    userId = message.from_user.id if message.from_user else chatId
    username = getUserName(message.from_user)
    text = message.text if message and message.text else ''
    args = text.strip().split()
    argsCount = len(args)
    if argsCount > 2:
        botApp.reply_to(message, emojies.error + ' Too many arguments.')
        return
    isCastCommand = args[0] == '/cast' if argsCount > 0 else False
    # Wait for the url in the next message
    if not argsCount or (isCastCommand and argsCount == 1):
        startWaitingForCastUrl(chat, message)
        return
    url = args[0]
    if isCastCommand and argsCount == 2:
        url = args[1]
    if not isYoutubeLink(url):
        botApp.reply_to(
            message,
            emojies.error + ' A youtube url has been expected to fetch a video from. But you\'ve sent "%s".' % url,
        )
        return
    downloadAndSendAudioToChat(url, chatId, username, message)
