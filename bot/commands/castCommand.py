# -*- coding:utf-8 -*-

import traceback
import telebot  # pyTelegramBotAPI
import re
import os

# Youtube download libraries
# import youtube_dl # @see https://github.com/ytdl-org/youtube-dl
import yt_dlp   # @see https://github.com/yt-dlp/yt-dlp

from core.helpers.errors import errorToString
from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig

from bot.botApp import botApp
from core.utils import debugObj


# @see https://github.com/ytdl-org/youtube-dl

YTDL = yt_dlp

logger = getLogger('bot/commands/cast')

demoVideo = 'https://www.youtube.com/watch?v=EngW7tLk6R8'

# Trace keys in logger and reponses
debugKeysList = [
    'url',
    #  'args',
    'text',
    'timeStr',
    'chatId',
    'username',
    'LOCAL',
    #  'YT_USERNAME',
    #  'YT_PASSWORD',
    #  'YT_COOKIE',
]


isYoutubeLink = re.compile(r'^https://\w*\.youtube.com/')

audioFileExt = '.mp3'

logTraceback = False


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
        video_info = YTDL.YoutubeDL().extract_info(url=url, download=False)
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

        # Use cookies (if provided):
        YT_COOKIE = appConfig.get('YT_COOKIE')
        ytCookieFile = filepath + '.cookie'
        if YT_COOKIE:
            logger.info('loadAudioFile: Found YT_COOKIE: %s' % YT_COOKIE)
            logger.info('loadAudioFile: Writing to ytCookieFile: %s' % ytCookieFile)
            YT_COOKIE = YT_COOKIE.strip()
            #  YTDL.cookies = YT_COOKIE
            # Writing cookie data to a file...
            with open(ytCookieFile, 'wb') as fh:
                fh.write(YT_COOKIE.strip().encode('utf-8'))

        # Prepare options:
        options = {
            # @see https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': filepath,
            'verbose': True,
            #  'extractor_args': 'youtube:player-client=web;po_token=web+PO_TOKEN_VALUE_HERE',
            #  'skip_download': True,  # ???
        }

        # Add cookie file
        if YT_COOKIE and ytCookieFile:
            options['cookiefile'] = ytCookieFile

        # Add PO Token (if exists), see https://github.com/yt-dlp/yt-dlp/wiki/Extractors#manually-acquiring-a-po-token-from-a-browser-for-use-when-logged-out
        YT_POTOKEN = appConfig.get('YT_POTOKEN')
        if YT_POTOKEN:
            logger.info('loadAudioFile: Using YT_POTOKEN: %s' % (YT_POTOKEN))
            options['extractor_args'] = 'youtube:player-client=web;po_token=web+' + YT_POTOKEN

        # Add authentication params...
        YT_USERNAME = appConfig.get('YT_USERNAME')
        YT_PASSWORD = appConfig.get('YT_PASSWORD')
        if YT_USERNAME and YT_PASSWORD:
            logger.info('loadAudioFile: Using username (%s) and password (%s)' % (YT_USERNAME, YT_PASSWORD))
            options['username'] = YT_USERNAME
            options['password'] = YT_PASSWORD

        # DEBUG: Show options...
        logger.info('loadAudioFile: Using options:\n%s' % debugObj(options))

        # Downloading...
        logger.info('loadAudioFile: Downloading...')
        with YTDL.YoutubeDL(options) as ydl:
            ydl.download([webpageUrl])
            # Done!
            logger.info('loadAudioFile: Success, the audio has loaded from url %s into file %s' % (url, filepath))
            return filepath
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Video download error: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            logger.info('loadAudioFile: Traceback for the following error:' + sTraceback)
        logger.error('loadAudioFile: ' + errMsg)
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
    botApp.reply_to(message, replyMsg)
    # Let's start...
    botApp.send_message(
        chatId, "Now we're trying to download the video and fetch the audio from it... Be patient, please."
    )
    try:
        # Load audio from url...
        result = loadAudioFile(url)
        logger.info('castCommand: Loaded: ' + result)
        botApp.send_message(chatId, 'Your audio file is: `%s`' % result)
        # TODO: Send audio to the bot
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        #  sTraceback = str(traceback.format_exc())
        errMsg = 'Error fetching audio: ' + errText
        logger.error('castCommand: ' + errMsg)
        botApp.reply_to(message, errMsg)
