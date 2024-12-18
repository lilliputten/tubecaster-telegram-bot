# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from core.appConfig import LOCAL, LOGGING_CHANNEL_ID, PROJECT_INFO, PROJECT_PATH, TELEGRAM_TOKEN, TELEGRAM_OWNER_ID

from core.helpers.time import formatTime, getTimeStamp
from core.logger import getLogger

from botApp import botApp
from core.utils import debugObj

from botCore import botConfig


logger = getLogger('botCommands/sendInfo')

commonInfoData = {
    'LOCAL': LOCAL,
    'PROJECT_INFO': PROJECT_INFO,
    'PROJECT_PATH': PROJECT_PATH,
    'WEBHOOK_URL': botConfig.WEBHOOK_URL,
    'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
}


def notifyOwner(text: str, logInfo: str | None = None):
    if logInfo:
        logger.info(logInfo)
    if LOGGING_CHANNEL_ID and not LOCAL:
        botApp.send_message(LOGGING_CHANNEL_ID, text)


def sendCommandInfo(message: telebot.types.Message):
    chat = message.chat

    text = message.text
    sticker = message.sticker
    stickerFileId = sticker.file_id if sticker else None
    stickerEmoji = sticker.emoji if sticker else None
    stickerSetName = sticker.set_name if sticker else None
    messageId = message.id
    contentType = message.content_type
    messageDate = formatTime(None, message.date)
    user = message.from_user
    userId = user.id if user else None
    #  username = user.username if user else None
    chatId = chat.id
    text = message.text
    username = chat.username
    json = message.json
    fromData: dict = json.get('from', {})
    languageCode = fromData.get('language_code')
    #  userId = fromData.get('id')
    commandHash = ' '.join(
        list(
            filter(
                None,
                [
                    contentType,
                    text,
                ],
            )
        )
    )
    obj = {
        'commandHash': commandHash,
        'contentType': contentType,
        'messageId': messageId,
        'text': text,
        'sticker': repr(sticker),
        'stickerFileId': stickerFileId,
        'stickerSetName': stickerSetName,
        'stickerEmoji': stickerEmoji,
        'timeStr': getTimeStamp(),
        'chatId': chatId,
        'userId': userId,
        #  'user': user,
        'username': username,
        #  'first_name': first_name,
        #  'last_name': last_name,
        'languageCode': languageCode,
        'messageDate': messageDate,
        **commonInfoData,
    }
    debugStr = debugObj(obj)
    logContent = '\n'.join(
        [
            'command: %s' % commandHash,
            debugStr,
        ]
    )
    content = '\n\n'.join(
        [
            'TubeCaster bot received a command: %s' % text,
            debugStr,
        ]
    )
    notifyOwner(content, logContent)


def sendQueryInfo(query: telebot.types.CallbackQuery):
    data = query.data  # 'startHelp'
    fromUser = query.from_user  # <telebot.types.User object at 0x000002B8D75517F0>
    gameShortName = query.game_short_name  # None
    id = query.id  # '2106243731802653912'
    inlineMessageId = query.inline_message_id  # None
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
            'TubeCaster bot received a query: %s' % data,
            debugStr,
        ]
    )
    notifyOwner(content, logContent)
