# -*- coding:utf-8 -*-

import traceback
import telebot  # pytelegrambotapi
import re
import youtube_dl
import os

from core.helpers.errors import errorToString
from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig

from bot.botApp import botApp
from core.utils import debugObj


# @see https://github.com/ytdl-org/youtube-dl


logger = getLogger('bot/commands/cast')

# Trace keys in logger and reponses
debugKeysList = [
    'url',
    'args',
    'text',
    'timeStr',
    'chatId',
    'username',
    'LOCAL',
]


isYoutubeLink = re.compile(r'^https://\w*\.youtube.com/')

audioFileExt = '.mp3'


def getFileIdFromName(name: str):
    filename = name.lower()
    filename = re.sub(r'\W+', ' ', filename).strip()
    filename = re.sub(r'\s+', '-', filename)
    return filename


def getFileIdFromUrl(url: str):
    filename = url
    filename = re.sub(r'^.*youtube.com/', '', filename)
    filename = getFileIdFromName(filename)
    return filename


def loadAudioFile(url):
    """
    Returns local temporarily saved audio file name.
    """
    try:
        logger.info('loadAudioFile: Loading video from url: %s' % url)
        #  url = input("please enter youtube video url:")
        video_info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)
        if not video_info:
            raise Exception('No video info has been returned')
        #  title = video_info['title']
        #  fileid = getFileIdFromName(title)
        fileid = getFileIdFromUrl(url)
        filename = 'temp-' + fileid + audioFileExt
        webpageUrl = video_info['webpage_url']
        cwd = os.getcwd()
        filepath = os.path.join(cwd, filename)
        print('filepath: %s' % filepath)
        options = {
            # @see https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': filepath,
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([webpageUrl])
            logger.info('loadAudioFile: Loaded audio from url %s to file %s' % (url, filepath))
            return filepath
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'Error loading video: ' + errText
        logger.error('loadAudioFile: ' + errMsg)
        print(sTraceback)
        raise Exception(errMsg)


@botApp.message_handler(commands=['cast'])
def castCommand(message: telebot.types.Message):
    # Get core parameters
    text = message.text
    chat = message.chat
    chatId = chat.id
    username = chat.username
    # Parse text
    if not text:
        botApp.reply_to(message, 'Some arguments expected.')
        return
    args = text.strip().split()
    argsCount = len(args) - 1
    if argsCount < 1:
        botApp.reply_to(message, 'Too few arguments.')
        return
    elif argsCount > 1:
        botApp.reply_to(message, 'Too many arguments.')
        return
    url = args[1]
    if not isYoutubeLink.match(url):
        botApp.reply_to(message, 'The url should be a valid youtube link (like `https://youtube.com/...`).')
        return
    # Ok, show info...
    obj = {
        **{
            'url': url,
            'args': ', '.join(args),
            'timeStr': getTimeStamp(True),
            'chatId': chatId,
            'username': username,
        },
        **appConfig,
    }
    debugData = debugObj(obj, debugKeysList)
    logContent = '\n\n'.join(
        [
            'castCommand',
            debugData,
        ]
    )
    replyMsg = '\n\n'.join(
        [
            'Ok, we\'ve got your video.',
            debugData,
        ]
    )
    logger.info(logContent)
    #  botApp.send_message(chatId, replyMsg)
    botApp.reply_to(message, replyMsg)
    # Lets, start...
    botApp.send_message(chatId, 'Now we\'re downloading and processing... Be patient, please.')
    try:
        # Load audio from url...
        result = loadAudioFile(url)
        logger.info('castCommand: Loaded: ' + result)
        botApp.send_message(chatId, 'Your audio file is: `%s`' % result)
        # TODO: Send audio to the bot
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'Error dosnloading audio for video: ' + errText
        logger.error('castCommand: ' + errMsg)
        print(sTraceback)
        botApp.reply_to(message, errMsg)
