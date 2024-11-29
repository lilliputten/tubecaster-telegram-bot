# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from core.helpers.errors import errorToString
from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig

from bot.botApp import botApp
from core.utils import debugObj

from .castHelpers import loadAudioFile, demoVideo

_logger = getLogger('bot/commands/castTestCommand')

# Trace keys in logger and reponses
_debugKeysList = [
    'url',
    #  'args',
    'text',
    'timeStr',
    'chatId',
    'username',
    '_LOCAL',
    #  'YT_USERNAME',
    #  'YT_PASSWORD',
    #  'YT_COOKIE',
]


@botApp.message_handler(commands=['castTest'])
def castTestCommand(message: telebot.types.Message):
    # Get core parameters
    text = message.text
    chat = message.chat
    chatId = chat.id
    username = chat.username
    # Parse text
    if not text:
        botApp.reply_to(message, 'Some arguments expected.')
        return
    url = demoVideo   # args[1]
    # Ok, show info...
    obj = {
        **{
            'url': url,
            'timeStr': getTimeStamp(True),
            'chatId': chatId,
            'username': username,
        },
        **appConfig,
    }
    debugData = debugObj(obj, _debugKeysList)
    logContent = '\n'.join(
        [
            'castTestCommand',
            debugData,
        ]
    )
    replyMsg = '\n\n'.join(
        [
            "Ok, we've got your video.",
            #  debugData,
        ]
    )
    _logger.info(logContent)
    botApp.reply_to(message, replyMsg)
    # Let's start...
    botApp.send_message(
        chatId, "Now we're trying to download the video and fetch the audio from it... Be patient, please."
    )
    try:
        # Load audio from url...
        audioFile = loadAudioFile(url)
        _logger.info('castTestCommand: Loaded: ' + audioFile)
        #  botApp.send_message(chatId, 'Your audio file is: `%s`' % audioFile)
        with open(audioFile, 'rb') as audio:
            botApp.send_audio(chatId, audio=audio)
        # TODO: Send audio to the bot
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        #  sTraceback = str(traceback.format_exc())
        errMsg = 'Error fetching audio: ' + errText
        _logger.error('castTestCommand: ' + errMsg)
        botApp.reply_to(message, errMsg)


__all__ = [
    'castTestCommand',
]
