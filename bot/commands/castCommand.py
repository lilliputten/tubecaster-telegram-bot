# -*- coding:utf-8 -*-

import posixpath
import traceback
import telebot  # pyTelegramBotAPI
import re
import os

from core.helpers.errors import errorToString

#  from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig

from bot.botApp import botApp

#  from core.utils import debugObj

from .castHelpers import downloadAndSendAudioToChat


# @see https://github.com/ytdl-org/youtube-dl

_logger = getLogger('bot/commands/castCommand')

demoVideo = 'https://www.youtube.com/watch?v=EngW7tLk6R8'

_LOCAL = appConfig.get('LOCAL')

# Use local 'temp' or vercel specific '/tmp' folders for temporarily files
tempPath = posixpath.join(os.getcwd(), 'temp') if _LOCAL else '/tmp'

#  # Trace keys in logger and reponses
#  _debugKeysList = [
#      'url',
#      #  'args',
#      'text',
#      'timeStr',
#      'chatId',
#      'username',
#      '_LOCAL',
#      #  'YT_USERNAME',
#      #  'YT_PASSWORD',
#      #  'YT_COOKIE',
#  ]


_isYoutubeLink = re.compile(r'^https://\w*\.youtube.com/')

#  _audioFileExt = '.mp3'
_logTraceback = False


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
        botApp.reply_to(message, 'Too few arguments. We are expecting youtube video url, like this: /cast URL.')
        return
    elif argsCount > 1:
        botApp.reply_to(message, 'Too many arguments.')
        return
    url = args[1]
    if not _isYoutubeLink.match(url):
        botApp.reply_to(message, 'The url should be a valid youtube link (like `https://youtube.com/...`).')
        return
    #  # Ok, show info...
    #  obj = {
    #      **{
    #          'url': url,
    #          'timeStr': getTimeStamp(True),
    #          'chatId': chatId,
    #          'username': username,
    #      },
    #      **appConfig,
    #  }
    #  debugData = debugObj(obj, _debugKeysList)
    #  logContent = '\n\n'.join(
    #      [
    #          'castCommand',
    #          debugData,
    #      ]
    #  )
    #  replyMsg = '\n\n'.join(
    #      [
    #          "Ok, we've've got your video and now are trying to download it and fetch the audio...",
    #          # 'Be patient, please.',
    #          #  debugData,
    #      ]
    #  )
    #  _logger.info(logContent)
    #  botApp.reply_to(message, replyMsg)
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
