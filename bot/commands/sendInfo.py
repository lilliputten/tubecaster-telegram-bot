# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from core.appConfig import appConfig, LOCAL, PROJECT_INFO, PROJECT_PATH

from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger
from bot.botApp import botApp
from core.utils import debugObj

from .. import botConfig


logger = getLogger('bot/commands')

commonInfoData = {
    'LOCAL': LOCAL,
    'PROJECT_INFO': PROJECT_INFO,
    'PROJECT_PATH': PROJECT_PATH,
    'WEBHOOK_URL': botConfig.WEBHOOK_URL,
    'TELEGRAM_TOKEN': appConfig.get('TELEGRAM_TOKEN'),
}


def notifyOwner(text: str, logInfo: str | None = None):
    if logInfo:
        logger.info(logInfo)
    if botConfig.TELEGRAM_OWNER_ID:
        botApp.send_message(botConfig.TELEGRAM_OWNER_ID, text)


def sendCommandInfo(message: telebot.types.Message):
    chat = message.chat
    chatId = chat.id
    text = message.text
    username = chat.username
    json = message.json
    fromData: dict = json.get('from', {})
    languageCode = fromData.get('language_code')
    #  userId = fromData.get('id')
    obj = {
        'text': text,
        'timeStr': getTimeStamp(True),
        'chatId': chatId,
        #  'userId': userId,
        'username': username,
        #  'first_name': first_name,
        #  'last_name': last_name,
        'languageCode': languageCode,
        **commonInfoData,
    }
    debugStr = debugObj(obj)
    logContent = '\n'.join(
        [
            'command: %s' % text,
            debugStr,
        ]
    )
    content = '\n\n'.join(
        [
            'Bot received a command: %s' % text,
            debugStr,
        ]
    )
    notifyOwner(content, logContent)


def sendQueryInfo(query: telebot.types.CallbackQuery):
    #  # query sample object:
    #  chat_instance = '-6344726803245517946'
    #  data = 'startHelp'
    #  from_user = <telebot.types.User object at 0x000002B8D75517F0>
    #  game_short_name = None
    #  id = '2106243731802653912'
    #  inline_message_id = None
    #  json = {'id': '2106243731802653912', 'from': {'id': 490398083, 'is_bot': False, 'first_name': 'Ig', 'username': 'lilliputten', 'language_code': 'en'}, 'message': {'message_id': 1049, 'from': {...}, 'chat': {...}, 'date': 1733007179, 'photo': [...], 'caption': 'Hi, Ig!\n\nWelcome to the TubeCaster bot!\n\nThe bot version is: v.0.0.7 / 2024.11.29 11:...an audio. Type /help to find all commands.', 'caption_entities': [...], 'reply_markup': {...}}, 'chat_instance': '-6344726803245517946', 'data': 'startHelp'}
    #  message = <telebot.types.Message object at 0x000002B8D6F12210>

    #  chatInstance = query.chat_instance  # '-6344726803245517946'
    data = query.data  # 'startHelp'
    fromUser = query.from_user  # <telebot.types.User object at 0x000002B8D75517F0>
    gameShortName = query.game_short_name  # None
    id = query.id  # '2106243731802653912'
    inlineMessageId = query.inline_message_id  # None
    #  json = query.json  # {'id': '2106243731802653912', 'from': {'id': 490398083, 'is_bot': False, 'first_name': 'Ig', 'username': 'lilliputten', 'language_code': 'en'}, 'message': {'message_id': 1049, 'from': {...}, 'chat': {...}, 'date': 1733007179, 'photo': [...], 'caption': 'Hi, Ig!\n\nWelcome to the TubeCaster bot!\n\nThe bot version is: v.0.0.7 / 2024.11.29 11:...an audio. Type /help to find all commands.', 'caption_entities': [...], 'reply_markup': {...}}, 'chat_instance': '-6344726803245517946', 'data': 'startHelp'}
    message = query.message  # <telebot.types.Message object at 0x000002B8D6F12210>

    userId = fromUser.id
    username = fromUser.username
    text = message.text if message else None

    obj = {
        'data': data,
        'text': text,
        'userId': userId,
        'username': username,
        #  'fromUser': fromUser,
        'gameShortName': gameShortName,
        'id': id,
        'inlineMessageId': inlineMessageId,
        #  'json': json, # It's too long
        #  'message': message,
        **commonInfoData,
    }
    debugStr = debugObj(obj)
    logContent = '\n'.join(
        [
            'query: %s' % data,
            debugStr,
        ]
    )
    content = '\n\n'.join(
        [
            'Bot received a query: %s' % data,
            debugStr,
        ]
    )
    notifyOwner(content, logContent)
