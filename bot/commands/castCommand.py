# -*- coding:utf-8 -*-

import traceback
import telebot  # pyTelegramBotAPI
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
    #  'YT_USERNAME',
    #  'YT_PASSWORD',
    'YT_COOKIE',
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
        logger.info('loadAudioFile: Started downloading video from url: %s' % url)

        # Extract video info
        video_info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)
        if not video_info:
            raise Exception('No video info has been returned')
        webpageUrl = video_info['webpage_url']
        logger.info('loadAudioFile: Got webpageUrl: %s' % webpageUrl)

        # Create file url:
        fileid = getFileIdFromUrl(url)
        filename = 'temp-' + fileid + audioFileExt
        cwd = os.getcwd()
        filepath = os.path.join(cwd, filename)
        logger.info('loadAudioFile: Prepared filepath: %s' % filepath)

        # Prepare cookies:
        YT_COOKIE = appConfig.get('YT_COOKIE')
        ytCookieFile = filepath + '.cookie'
        if YT_COOKIE:
            logger.info('loadAudioFile: Found YT_COOKIE: %s' % YT_COOKIE)
            logger.info('loadAudioFile: Writing to ytCookieFile: %s' % YT_COOKIE)
            # Writing cookie data to a file...
            with open(ytCookieFile, 'wb') as fh:
                fh.write(YT_COOKIE.strip().encode('utf-8'))

        # Prepare options:
        options = {
            # @see https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': filepath,
            'skip_download': True,  # ???
            #  'username': appConfig.get('YT_USERNAME'),
            #  'password': appConfig.get('YT_PASSWORD'),
            #  'cookiefile': 'youtube_cookies.txt',  # https://www.reddit.com/r/youtubedl/comments/1e6bzu4/comment/lod50pa
        }
        if YT_COOKIE:
            options['cookiefile'] = ytCookieFile
        logger.info('loadAudioFile: Using options: %s' % debugObj(options))

        # Downloading...
        logger.info('loadAudioFile: Downloading...')
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([webpageUrl])
            # Done!
            logger.info('loadAudioFile: Loaded audio from url %s to file %s' % (url, filepath))
            return filepath
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'Video download error: ' + errText
        logger.error('loadAudioFile: ' + errMsg + '\n\n' + sTraceback + '\n\n')
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
            "Ok, we've got your video.",
            debugData,
        ]
    )
    logger.info(logContent)
    #  botApp.send_message(chatId, replyMsg)
    botApp.reply_to(message, replyMsg)
    # Lets, start...
    botApp.send_message(chatId, "Now we're trying to download the video and fetch the audio from it... Be patient, please.")
    try:
        # Load audio from url...
        result = loadAudioFile(url)
        logger.info('castCommand: Loaded: ' + result)
        botApp.send_message(chatId, 'Your audio file is: `%s`' % result)
        # TODO: Send audio to the bot
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'Error fetching audio: ' + errText
        logger.error('castCommand: ' + errMsg)
        print(sTraceback)
        botApp.reply_to(message, errMsg)
