# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
import traceback

from core.helpers.errors import errorToString

#  from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger

#  from core.appConfig import appConfig

from bot.botApp import botApp

#  from core.utils import debugObj

from .castHelpers import demoVideo, downloadAndSendAudioToChat

_logger = getLogger('bot/commands/castTestCommand')

_logTraceback = False

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


@botApp.message_handler(commands=['castTest'])
def castTestCommand(message: telebot.types.Message):
    #  timeStr = getTimeStamp()
    # Get core parameters
    #  text = str(message.text)
    #  chat = message.chat
    #  chatId = chat.id
    #  username = str(chat.username)
    url = demoVideo   # args[1]
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
    #  logContent = '\n'.join(
    #      [
    #          'castTestCommand',
    #          debugData,
    #      ]
    #  )
    #  replyMsg = '\n\n'.join(
    #      [
    #          "Ok, we've've got your video and now are trying to download it and fetch the audio...",
    #          #  debugData,
    #      ]
    #  )
    #  _logger.info(logContent)
    #  botApp.reply_to(message, replyMsg)
    # Let's start...
    try:
        downloadAndSendAudioToChat(url, message)   # username, chatId)
        #  # Prepare...
        #  options, videoInfo = prepareAudioFile(url, username)
        #  # Load audio from url...
        #  audioFile = downloadAudioFile(options, videoInfo)
        #  if not audioFile:
        #      raise Exception('Audio file name hasn not been set')
        #  _logger.info('castTestCommand: Loaded: ' + audioFile)
        #  #  botApp.send_message(chatId, 'Your audio file is: `%s`' % audioFile)
        #  with open(audioFile, 'rb') as audio:
        #      # send_audio params:
        #      #  chat_id: int | str,
        #      #  audio: Any | str,
        #      #  caption: str | None = None,
        #      #  duration: int | None = None,
        #      #  performer: str | None = None,
        #      #  title: str | None = None,
        #      #  reply_to_message_id: int | None = None,
        #      #  reply_markup: REPLY_MARKUP_TYPES | None = None,
        #      #  parse_mode: str | None = None,
        #      #  disable_notification: bool | None = None,
        #      #  timeout: int | None = None,
        #      #  thumbnail: Any | str | None = None,
        #      #  caption_entities: List[MessageEntity] | None = None,
        #      #  allow_sending_without_reply: bool | None = None,
        #      #  protect_content: bool | None = None,
        #      #  message_thread_id: int | None = None,
        #      #  thumb: Any | str | None = None,
        #      #  reply_parameters: ReplyParameters | None = None,
        #      #  business_connection_id: str | None = None,
        #      #  message_effect_id: str | None = None,
        #      #  allow_paid_broadcast: bool | None = None
        #      botApp.send_audio(
        #          chatId,
        #          audio=audio,
        #          caption=videoInfo['title'],
        #          thumbnail=videoInfo['thumbnail'],
        #      )
        #  # Remove temporarily files and folders
        #  cleanFiles(options)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'Error fetching audio: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('castTestCommand: Traceback for the following error:' + sTraceback)
        _logger.error('castTestCommand: ' + errMsg)
        botApp.reply_to(message, errMsg)


__all__ = [
    'castTestCommand',
]
