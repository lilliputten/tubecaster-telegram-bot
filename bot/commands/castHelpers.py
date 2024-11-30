# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
from typing import TypedDict, Optional
import traceback
import re
import os
import posixpath
import pathlib

# Youtube download libraries
# import youtube_dl # @see https://github.com/ytdl-org/youtube-dl
import yt_dlp   # @see https://github.com/yt-dlp/yt-dlp

from core.helpers.errors import errorToString
from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger
from core.appConfig import appConfig
from bot.botApp import botApp

from core.utils import debugObj

from .. import botConfig


# Eg: /cast https://www.youtube.com/watch?v=EngW7tLk6R8

demoVideo = 'https://www.youtube.com/watch?v=EngW7tLk6R8'   # Short vide, 00:05
#  demoVideo = 'https://www.youtube.com/watch?v=UdaQRvVTIqU'   # Video with a russian title, 02:47
#  demoVideo = 'https://www.youtube.com/watch?v=eBHLST0pLXg'   # Video with a russian title, 00:18
#  # Last video with a playlist
#  demoVideo = 'https://www.youtube.com/watch?v=eBHLST0pLXg&list=PLuDoUpt1iJ4XHDwHJm7xjFLiYJXTf4ouv&index=3'

_YTDL = yt_dlp

_logger = getLogger('bot/commands/castHelpers')

_LOCAL = appConfig.get('LOCAL')

# Use local 'temp' or vercel specific '/tmp' folders for temporarily files
_tempPath = (
    posixpath.join(pathlib.Path(os.getcwd()).as_posix(), 'temp') if _LOCAL or not botConfig.IS_VERCEL else '/tmp'
)

_audioFileExt = ''   # '.mp3'

_logTraceback = False

_isYoutubeLink = re.compile(r'^https://\w*\.youtube.com/')


def getIdFromName(name: str):
    filename = name   # .lower()
    filename = re.sub(r'\W+', ' ', filename).strip()
    #  filename = re.sub(r'\s+', '-', filename)
    return filename


def getFileIdFromUrl(url: str, username: str):
    filename = url
    filename = re.sub(r'^.*youtube.com/', '', filename)
    filename = getIdFromName(filename)
    filename = re.sub(r'^watch-v-', '', filename)
    if username:
        filename = getIdFromName(username) + '-' + filename
    return filename


#  type OptionsType = dict[str, str | bool | int | None]
class OptionsType(TypedDict):
    cachedir: str
    extractor_args: Optional[str]
    outtmpl: Optional[str]
    _destFolder: Optional[str]
    _destFile: Optional[str]
    cookiefile: Optional[str]
    format: Optional[str]
    keepvideo: Optional[bool]
    verbose: Optional[bool]
    noplaylist: Optional[bool]
    #  debug_printtraffic: Optional[bool]


def getYtdlBaseOptions():
    # Prepare options:
    options: OptionsType = {
        # @see https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
        'verbose': True,
        'cachedir': _tempPath,
        'verbose': True,
        'noplaylist': True,
        'keepvideo': False,
        'extractor_args': None,
        'outtmpl': None,
        '_destFolder': None,
        '_destFile': None,
        'cookiefile': None,
        'format': None,
        #  'debug_printtraffic': None,
    }

    # Add PO Token (if exists), see https://github.com/yt-dlp/yt-dlp/wiki/Extractors#manually-acquiring-a-po-token-from-a-browser-for-use-when-logged-out
    YT_POTOKEN = appConfig.get('YT_POTOKEN')
    if YT_POTOKEN:
        _logger.info('getYtdlBaseOptions: Using YT_POTOKEN: %s' % (YT_POTOKEN))
        options['extractor_args'] = 'youtube:player-client=web;po_token=web+' + YT_POTOKEN

    #  # Add authentication params (NOTE: Unused as not supported)
    #  YT_USERNAME = appConfig.get('YT_USERNAME')
    #  YT_PASSWORD = appConfig.get('YT_PASSWORD')
    #  if YT_USERNAME and YT_PASSWORD:
    #      _logger.info('getYtdlBaseOptions: Using username (%s) and password (***)' % (YT_USERNAME))
    #      options['username'] = YT_USERNAME
    #      options['password'] = YT_PASSWORD

    return options


def prepareLinkInfo(url: str, username: str):
    """
    Returns local temporarily saved audio file name.
    """
    try:
        _logger.info('prepareAudioFile: Trying to get an info for the video url: %s' % url)

        # Prepare options...
        options = getYtdlBaseOptions()

        folderName = getTimeStamp('id') + '-' + username
        destFolder = options['_destFolder'] = posixpath.join(_tempPath, folderName)
        # Ensure temp folder is exists
        pathlib.Path(destFolder).mkdir(parents=True, exist_ok=True)

        # DEBUG: Show options...
        _logger.info('prepareAudioFile: Fetching info with options:\n%s' % debugObj(dict(options)))

        # Extract video info
        videoInfo = _YTDL.YoutubeDL(options).extract_info(url=url, download=False)
        if not videoInfo:
            raise Exception('No video info has been returned')

        # Create file url:
        title = videoInfo['title']
        fileId = getIdFromName(title) if title else getFileIdFromUrl(url, username)
        filename = fileId + _audioFileExt
        destFile = posixpath.join(destFolder, filename)
        _logger.info('prepareAudioFile: Computed destFile file name: %s' % destFile)

        # Set destination file name
        options['outtmpl'] = destFile
        options['_destFile'] = destFile

        # Use cookies (if provided):
        YT_COOKIE = appConfig.get('YT_COOKIE')
        if YT_COOKIE:
            _logger.info('prepareAudioFile: Found YT_COOKIE: %s' % '***')
            YT_COOKIE = YT_COOKIE
            cookieFile = destFile + '.cookie'
            options['cookiefile'] = cookieFile
            # Writing cookie data to a file, if it's absent...
            _logger.info('prepareAudioFile: Writing cookieFile: %s' % cookieFile)
            with open(cookieFile, 'w') as fh:
                fh.write(YT_COOKIE.strip())

        return options, videoInfo
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Prepare audio file error: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('prepareAudioFile: Traceback for the following error:' + sTraceback)
        _logger.error('prepareAudioFile: ' + errMsg)
        raise Exception(errMsg)


def downloadAudioFile(options: OptionsType, videoInfo):
    """
    Returns local temporarily saved audio file name.
    """
    try:
        webpageUrl = videoInfo['webpage_url']
        _logger.info('downloadAudioFile: Trying to fetch a video via the url: %s' % webpageUrl)

        destFile = options['_destFile']

        # Extend options for download:
        options = {
            **options,
            # @see https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
            'format': 'bestaudio/best',
            'keepvideo': False,
            'verbose': True,
            #  'outtmpl': destFIle,
            #  'simulate': True,
            #  'skip_download': True,
            #  'check_formats': False,
            #  'ignoreerrors': True,
        }
        # DEBUG: Show options...
        _logger.info('downloadAudioFile: Downloading with options:\n%s' % debugObj(dict(options)))

        # Downloading...
        with _YTDL.YoutubeDL(options) as ydl:
            ydl.download([webpageUrl])  # BUG: It fails silently here for vercel serverless funciton
            # Done!
            _logger.info(
                'downloadAudioFile: Success, the audio has loaded from url %s into file %s' % (webpageUrl, destFile)
            )
            return destFile
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Audio download error: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('downloadAudioFile: Traceback for the following error:' + sTraceback)
        _logger.error('downloadAudioFile: ' + errMsg)
        raise Exception(errMsg)


def sizeofFmt(num, suffix='B'):
    #  if num == 0:
    #      return '0'
    if not num:
        return ''
    for unit in ('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z'):
        if abs(num) < 1024.0:
            return f'{num:3.1f}{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}Yi{suffix}'


def downloadAndSendAudioToChat(url: str, message: telebot.types.Message):
    chat = message.chat
    chatId = chat.id
    username = str(chat.username)

    if not _isYoutubeLink.match(url):
        botApp.reply_to(message, 'The url should be a valid youtube link.')
        return

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
            'downloadAndSendAudioToChat',
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
    botApp.reply_to(message, replyMsg)

    # Prepare...
    options, videoInfo = prepareLinkInfo(url, username)

    #  title = videoInfo['title']
    filesize = videoInfo['filesize']
    filesizeApprox = videoInfo['filesize_approx']
    sizeFmt = sizeofFmt(filesize if filesize else filesizeApprox)

    #  infoMsg = f'Going to start downloading the video "{title}" of size ({sizeFmt})...'
    infoMsg = ''.join(
        list(
            filter(
                None,
                [
                    'Ok, downloading the video',
                    f' ({sizeFmt})' if sizeFmt else '',
                    '...',
                ],
            )
        )
    )
    botApp.reply_to(message, infoMsg)

    try:
        # Load audio from url...
        audioFile = downloadAudioFile(options, videoInfo)
        if not audioFile:
            raise Exception('Audio file name has not been defined')
        audioSize = os.path.getsize(audioFile)
        audioSizeFmt = sizeofFmt(audioSize)
        _logger.info(f'castCommand: Audio file {audioFile} (with size: {audioSizeFmt}) has been downloaded')
        infoMsg = ''.join(
            list(
                filter(
                    None,
                    [
                        'Ok, sending the audio',
                        f' ({audioSizeFmt})' if audioSizeFmt else '',
                        '...',
                    ],
                )
            )
        )
        botApp.reply_to(message, infoMsg)
        #  botApp.send_message(chatId, 'Your audio file is: `%s`' % audioFile)
        with open(audioFile, 'rb') as audio:
            # send_audio params:
            #  chat_id: int | str,
            #  audio: Any | str,
            #  caption: str | None = None,
            #  duration: int | None = None,
            #  performer: str | None = None,
            #  title: str | None = None,
            #  reply_to_message_id: int | None = None,
            #  reply_markup: REPLY_MARKUP_TYPES | None = None,
            #  parse_mode: str | None = None,
            #  disable_notification: bool | None = None,
            #  timeout: int | None = None,
            #  thumbnail: Any | str | None = None,
            #  caption_entities: List[MessageEntity] | None = None,
            #  allow_sending_without_reply: bool | None = None,
            #  protect_content: bool | None = None,
            #  message_thread_id: int | None = None,
            #  thumb: Any | str | None = None,
            #  reply_parameters: ReplyParameters | None = None,
            #  business_connection_id: str | None = None,
            #  message_effect_id: str | None = None,
            #  allow_paid_broadcast: bool | None = None
            botApp.send_audio(
                chatId,
                audio=audio,
                caption=videoInfo['title'],
                duration=videoInfo['duration'],
                thumb=videoInfo['thumbnail'],
            )
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Video download error: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('downloadAndSendAudioToChat: Traceback for the following error:' + sTraceback)
        _logger.error('downloadAndSendAudioToChat: ' + errMsg)
        raise Exception(errMsg)
    finally:
        # Remove temporarily files and folders
        cleanFiles(options)


def cleanFiles(options: OptionsType):
    """
    Clean temporarily files and folders created in prepareAudioFile, downloadAudioFile
    """
    cookieFile = options['cookiefile']
    destFile = options['_destFile']
    destFolder = options['_destFolder']
    if cookieFile:
        pathlib.Path(cookieFile).unlink(missing_ok=True)
    if destFile:
        pathlib.Path(destFile).unlink(missing_ok=True)
    if destFolder and os.path.isdir(destFolder):
        dir = os.listdir(destFolder)
        # If it's empty...
        if not len(dir):
            # ...remove it
            pathlib.Path(destFolder).rmdir()


__all__ = [
    'demoVideo',
    'prepareLinkInfo',
    'downloadAudioFile',
    'downloadAndSendAudioToChat',
    'cleanFiles',
]
