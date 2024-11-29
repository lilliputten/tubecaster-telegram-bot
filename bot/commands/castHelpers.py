# -*- coding:utf-8 -*-

import traceback
import re
import os

# Youtube download libraries
# import youtube_dl # @see https://github.com/ytdl-org/youtube-dl
import yt_dlp   # @see https://github.com/yt-dlp/yt-dlp

from core.helpers.errors import errorToString
from core.logger import getLogger
from core.appConfig import appConfig

from core.utils import debugObj


demoVideo = 'https://www.youtube.com/watch?v=EngW7tLk6R8'

_YTDL = yt_dlp

_logger = getLogger('bot/commands/castCommand')

_LOCAL = appConfig.get('LOCAL')

# Use local 'temp' or vercel specific '/tmp' folders for temporarily files
_tempPath = os.path.join(os.getcwd(), 'temp') if _LOCAL else '/tmp'

# Trace keys in logger and reponses
debugKeysList = [
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


#  _isYoutubeLink = re.compile(r'^https://\w*\.youtube.com/')

_audioFileExt = '.mp3'

_logTraceback = False


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


def getYtdlBaseOptions(cookieFile: str):
    # Prepare options:
    options: dict[str, str | bool | int | None] = {
        # @see https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
        'verbose': True,
        'cachedir': _tempPath,
        #  'debug_printtraffic': True,
    }

    # Add cookie file
    if cookieFile:
        options['cookiefile'] = cookieFile

    # Add PO Token (if exists), see https://github.com/yt-dlp/yt-dlp/wiki/Extractors#manually-acquiring-a-po-token-from-a-browser-for-use-when-logged-out
    YT_POTOKEN = appConfig.get('YT_POTOKEN')
    if YT_POTOKEN:
        _logger.info('loadAudioFile: Using YT_POTOKEN: %s' % (YT_POTOKEN))
        options['extractor_args'] = 'youtube:player-client=web;po_token=web+' + YT_POTOKEN

    #  # Add authentication params (NOTE: Unused as not supported)
    #  YT_USERNAME = appConfig.get('YT_USERNAME')
    #  YT_PASSWORD = appConfig.get('YT_PASSWORD')
    #  if YT_USERNAME and YT_PASSWORD:
    #      _logger.info('loadAudioFile: Using username (%s) and password (***)' % (YT_USERNAME))
    #      options['username'] = YT_USERNAME
    #      options['password'] = YT_PASSWORD

    return options


def loadAudioFile(url):
    """
    Returns local temporarily saved audio file name.
    """
    try:
        _logger.info('loadAudioFile: Trying to fetch a video from the url: %s' % url)

        # Create file url:
        fileid = getFileIdFromUrl(url)
        filename = fileid + _audioFileExt
        destFIle = os.path.join(_tempPath, filename)
        _logger.info('loadAudioFile: Prepared destFIle file name: %s' % destFIle)
        cookieFile = ''

        # Use cookies (if provided):
        YT_COOKIE = appConfig.get('YT_COOKIE')
        if YT_COOKIE:
            _logger.info('loadAudioFile: Found YT_COOKIE: %s' % '***')   # YT_COOKIE)
            cookieFile = destFIle + '.cookie'
            _logger.info('loadAudioFile: Writing cookieFile: %s' % cookieFile)
            YT_COOKIE = YT_COOKIE
            # Writing cookie data to a file...
            with open(cookieFile, 'w') as fh:
                fh.write(YT_COOKIE.strip())

        # Prepare options for information fetch...
        options = getYtdlBaseOptions(cookieFile)

        # DEBUG: Show options...
        _logger.info('loadAudioFile: Fetching info with options:\n%s' % debugObj(options))

        # Extract video info
        video_info = _YTDL.YoutubeDL(options).extract_info(url=url, download=False)
        if not video_info:
            raise Exception('No video info has been returned')
        webpageUrl = video_info['webpage_url']
        _logger.info('loadAudioFile: Got webpageUrl: %s' % webpageUrl)

        # Extend options for download:
        options = {
            **options,
            # @see https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': destFIle,
            'verbose': True,
            #  'simulate': True,
            #  'skip_download': True,
            #  'check_formats': False,
            #  'ignoreerrors': True,
        }

        # DEBUG: Show options...
        _logger.info('loadAudioFile: Downloading with options:\n%s' % debugObj(options))

        # Downloading...
        with _YTDL.YoutubeDL(options) as ydl:
            #  ydl.download([webpageUrl])  # BUG: It fails silently here
            # Done!
            _logger.info('loadAudioFile: Success, the audio has loaded from url %s into file %s' % (url, destFIle))
            return destFIle
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Video download error: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('loadAudioFile: Traceback for the following error:' + sTraceback)
        _logger.error('loadAudioFile: ' + errMsg)
        raise Exception(errMsg)


__all__ = [
    'loadAudioFile',
    'demoVideo',
]
