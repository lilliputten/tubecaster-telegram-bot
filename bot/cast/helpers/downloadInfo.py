# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from core.helpers.files import youtubeLinkPrefix
from core.helpers.time import getTimeStamp
from core.logger import getLogger
from core.utils import debugObj

from bot import botApp
from bot.helpers import replyOrSend

from ..helpers.prepareLinkInfo import prepareLinkInfo

_logger = getLogger('bot/cast/downloadInfo')


def downloadInfo(url: str, chat: telebot.types.Chat, message: telebot.types.Message | None = None):
    chatId = chat.id
    username = str(chat.username)

    if not youtubeLinkPrefix.match(url):
        raise Exception('The url should be a valid youtube link. But we got: %s' % url)

    # Start...
    obj = {
        'url': url,
        'timeStr': getTimeStamp(True),
        'chatId': chatId,
        'username': username,
    }
    debugData = debugObj(obj)
    logContent = '\n'.join(
        [
            'downloadInfo',
            debugData,
        ]
    )
    replyMsg = '\n\n'.join(
        [
            'Ok, fetching your video details...',
            #  debugData,
        ]
    )
    _logger.info(logContent)
    replyOrSend(botApp, replyMsg, chat.id, message)

    return prepareLinkInfo(url, username)
