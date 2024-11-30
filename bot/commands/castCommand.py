# -*- coding:utf-8 -*-

from functools import partial
import pathlib
import posixpath
import traceback
import telebot  # pyTelegramBotAPI
import os

from core.helpers.errors import errorToString

#  from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig

from bot.botApp import botApp

from core.utils import debugObj

from .castHelpers import downloadAndSendAudioToChat


# @see https://github.com/ytdl-org/youtube-dl

_logger = getLogger('bot/commands/castCommand')

demoVideo = 'https://www.youtube.com/watch?v=EngW7tLk6R8'

_LOCAL = appConfig.get('LOCAL')

# Use local 'temp' or vercel specific '/tmp' folders for temporarily files
tempPath = posixpath.join(pathlib.Path(os.getcwd()).as_posix(), 'temp') if _LOCAL else '/tmp'

#  _audioFileExt = '.mp3'
_logTraceback = False


def processUrl(debugInfo: str, message: telebot.types.Message):
    text = message.text
    chat = message.chat
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
        'debugInfo': debugInfo,
    }
    debugStr = debugObj(obj)
    content = '\n\n'.join(
        [
            'processUrl: Start',
            debugStr,
        ]
    )
    _logger.info(content)
    botApp.reply_to(message, content)
    # Let's start...
    try:
        downloadAndSendAudioToChat(url, message)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'Error fetching audio: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('processUrl: Traceback for the following error:' + sTraceback)
        _logger.error('processUrl: ' + errMsg)
        botApp.reply_to(message, errMsg)


@botApp.message_handler(commands=['cast'])
def castCommand(message: telebot.types.Message):
    # Get core parameters
    text = message.text
    #  chat = message.chat
    #  chatId = chat.id
    #  username = str(chat.username)
    # Parse text
    if not text:
        botApp.reply_to(message, 'Some arguments expected.')
        return
    args = text.strip().split()
    argsCount = len(args) - 1
    if argsCount < 1:
        #  botApp.reply_to(message, 'Too few arguments. We are expecting youtube video url, like this: /cast URL.')
        replyMsg = 'Ok, now send the video address:'
        botApp.reply_to(message, replyMsg)
        debugInfo = 'test'
        botApp.register_next_step_handler(message, partial(processUrl, debugInfo))
        return
    elif argsCount > 1:
        botApp.reply_to(message, 'Too many arguments.')
        return
    url = args[1]
    # Let's start...
    try:
        downloadAndSendAudioToChat(url, message)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'Error fetching audio: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('castCommand: Traceback for the following error:' + sTraceback)
        _logger.error('castCommand: ' + errMsg)
        botApp.reply_to(message, errMsg)
