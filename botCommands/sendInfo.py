# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from botApp import botApp
from botCore.helpers import getUserName
from core.appConfig import LOCAL  # TELEGRAM_TOKEN,; TELEGRAM_OWNER_ID,
from core.appConfig import LOGGING_CHANNEL_ID, PROJECT_INFO, PROJECT_PATH
from core.helpers.strings import removeAnsiStyles
from core.helpers.time import formatTime, getTimeStamp
from core.logger import getDebugLogger, secondaryStyle, titleStyle
from core.utils import debugObj
from core.utils.generic import prepareLongString

# from botCore import botConfig

_maxHashLength = 100

_logger = getDebugLogger()

_commonInfoData = {
    'LOCAL': LOCAL,
    'PROJECT_INFO': PROJECT_INFO,
    'PROJECT_PATH': PROJECT_PATH,
    # 'WEBHOOK_URL': botConfig.WEBHOOK_URL,
    # 'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
}


def notifyOwner(text: str, logInfo: str | None = None):
    if logInfo:
        _logger.info(logInfo)
    if LOGGING_CHANNEL_ID:   # and not LOCAL:
        botApp.send_message(LOGGING_CHANNEL_ID, removeAnsiStyles(text))


def sendCommandInfo(message: telebot.types.Message, info: str | None = None):
    #  chat = message.chat
    chatId = message.chat.id
    text = message.text
    sticker = message.sticker
    stickerFileId = sticker.file_id if sticker else None
    stickerEmoji = sticker.emoji if sticker else None
    stickerSetName = sticker.set_name if sticker else None
    messageId = message.id
    contentType = message.content_type
    messageDate = formatTime(None, message.date)
    user = message.from_user
    userId = user.id if user else chatId
    text = prepareLongString(message.text, _maxHashLength)
    usernameStr = getUserName(user)
    json = message.json
    fromData: dict = json.get('from', {})
    languageCode = fromData.get('language_code')
    stateValue = botApp.get_state(userId, chatId)
    # fmt: off
    commandHash = ' '.join(list(filter(None, [
        info,
        contentType,
        text,
    ])))
    # fmt: on
    obj = {
        'timeStr': getTimeStamp(),
        'commandHash': commandHash,
        'contentType': contentType,
        'messageId': messageId,
        'text': text,
        'sticker': repr(sticker),
        'stickerFileId': stickerFileId,
        'stickerSetName': stickerSetName,
        'stickerEmoji': stickerEmoji,
        'userId': userId,
        'usernameStr': usernameStr,
        'languageCode': languageCode,
        'messageDate': messageDate,
        'stateValue': stateValue if stateValue else 'None',
        **_commonInfoData,
    }
    debugStr = debugObj(obj)
    logItems = [
        titleStyle('sendCommandInfo: %s' % commandHash),
        secondaryStyle(debugStr),
    ]
    logContent = '\n'.join(logItems)
    msgItems = [
        'TubeCaster bot received a command: %s' % text,
        secondaryStyle(debugStr),
    ]
    content = '\n\n'.join(msgItems)
    notifyOwner(content, logContent)


def sendQueryInfo(query: telebot.types.CallbackQuery, info: str | None = None):
    data = query.data  # 'startHelp'
    user = query.from_user  # <telebot.types.User object at 0x000002B8D75517F0>
    gameShortName = query.game_short_name  # None
    id = query.id  # '2106243731802653912'
    inlineMessageId = query.inline_message_id  # None
    message = query.message  # <telebot.types.Message object at 0x000002B8D6F12210>
    chatId = message.chat.id
    userId = user.id if user else chatId
    stateValue = botApp.get_state(userId, chatId)

    userId = user.id
    usernameStr = getUserName(user)
    text = prepareLongString(message.text, _maxHashLength)  if message else None

    # fmt: off
    queryHash = ' '.join(list(filter(None, [
        info,
        text,
    ])))
    # fmt: on

    obj = {
        'timeStr': getTimeStamp(),
        'queryHash': queryHash,
        'data': data,
        'text': text,
        'userId': userId,
        'usernameStr': usernameStr,
        'gameShortName': gameShortName,
        'id': id,
        'inlineMessageId': inlineMessageId,
        #  'json': json, # It's too long
        'message': repr(message),
        'stateValue': stateValue if stateValue else 'None',
        **_commonInfoData,
    }
    debugStr = debugObj(obj)
    logItems = [
        'sendQueryInfo: %s' % data,
        secondaryStyle(debugStr),
    ]
    logContent = '\n'.join(logItems)
    content = '\n\n'.join(
        [
            'TubeCaster bot received a query: %s' % queryHash,
            secondaryStyle(debugStr),
        ]
    )
    notifyOwner(content, logContent)
