# -*- coding:utf-8 -*-

import re
import time
import traceback
from random import uniform

from telebot import types

from botCore.constants import emojies
from botCore.helpers import editOrSendMessage, getVideoDetailsStr
from botCore.types import TVideoInfo, YtdlOptionsType
from core.helpers.errors import errorToString
from core.helpers.strings import removeAnsiStyles
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, primaryStyle, secondaryStyle, titleStyle, warningStyle
from core.utils import debugObj

from ..config.castConfig import YTDL, logTraceback

_logger = getDebugLogger()


def downloadAudioFile(
    options: YtdlOptionsType,
    videoInfo: TVideoInfo,
    chatId: str | int | None = None,
    rootMessage: types.Message | None = None,
):
    """
    Returns local temporary saved audio file name.
    """
    from botCommands.sendInfo import notifyOwner

    videoDetails = getVideoDetailsStr(videoInfo)
    videoDetailsStr = f' ({videoDetails})' if videoDetails else ''
    try:
        webpageUrl = videoInfo.get('webpage_url')
        _logger.info('downloadAudioFile: Trying to fetch an audio via the url: %s' % webpageUrl)

        destFile = options.get('_destFile')
        if not destFile:
            raise ValueError("'_destFile' option is required")

        # NOTE 2024.12.10, 07:30: This code produces an error: Requested format is not available. Use --list-formats for a list of available formats
        #  addCookieToOptions(options)

        # Extend options for download with fallback formats
        download_options: YtdlOptionsType = {
            **options,
            # @see https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
            'format': 'worstaudio/worst',
            # 'format': 'bestaudio/best',
            # 'format': 'bestaudio[format_note*=original]/bestaudio',  # Trying to get an original audio track
            # 'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio/best[height<=720]/best',
            'keepvideo': False,
            'verbose': True,
            #  'outtmpl': destFIle,
            #  'simulate': True,
            #  'skip_download': True,
            #  'check_formats': False,
            #  'ignoreerrors': True,
            # 2025.10.14, 14:44 -- Added by Amazon Q, trying to fix the "downloaded file is empty" error
            'extractor_retries': 3,
            'fragment_retries': 3,
            'retry_sleep_functions': {'http': lambda n: 2**n},
        }
        # DEBUG: Show options...
        _logger.info('downloadAudioFile: Downloading with options:\n%s' % debugObj(dict(download_options)))

        # # Downloading (the old approach: a single attempt)...
        # with YTDL.YoutubeDL(options) as ydl:   # type: ignore
        #     ydl.download([webpageUrl])   # type: ignore
        #     # Done!
        #     _logger.info(
        #         'downloadAudioFile: Success, the audio has loaded from url %s into file %s' % (webpageUrl, destFile)
        #     )
        #     return destFile

        # Downloading with retry logic for YouTube's anti-bot patterns...
        maxRetries = 5  # Increased to handle typical YouTube blocking patterns
        for attempt in range(maxRetries):
            try:
                infoItems = [
                    emojies.waiting + ' Downloading audio from the video',
                    videoDetailsStr,
                    f', attempt {attempt + 1}/{maxRetries}' if attempt else '',
                    '...',
                ]
                infoContent = ''.join(filter(None, infoItems))
                notifyOwner('downloadAudioFile: %s' % infoContent)
                editOrSendMessage(
                    infoContent,
                    chatId,
                    rootMessage,
                )

                with YTDL.YoutubeDL(download_options) as ydl:  # type: ignore
                    ydl.download([webpageUrl])  # type: ignore
                    # Done!
                    notifyOwner(
                        'downloadAudioFile: Success, the audio has loaded from url %s into file %s (attempt %d)'
                        % (webpageUrl, destFile, attempt + 1)
                    )
                    return destFile
            except Exception as err:
                errText = re.sub('[\n\r]+', ' ', errorToString(err, show_stacktrace=False))
                is403Error = '403' in errText or 'Forbidden' in errText
                isRetryable = (
                    is403Error
                    or 'HTTP Error' in errText
                    or 'Use --list-formats' in errText
                    # or 'The downloaded file is empty' in errText
                    # or 'fragment not found' in errText
                    # or 'nsig extraction failed' in errText
                )

                if isRetryable and attempt < maxRetries - 1:
                    # Use longer delays for YouTube's rate limiting patterns
                    baseDelay = 3 + (attempt * 2)  # 3s, 5s, 7s, 9s
                    waitTime = baseDelay + uniform(0, 2)  # Add jitter
                    notifyOwner(
                        f'downloadAudioFile: Attempt {attempt + 1} failed ({errText[:100]}...), retrying in {waitTime:.1f}s'
                    )
                    time.sleep(waitTime)
                    continue
                else:
                    # Re-raise the exception if not retryable or exhausted retries
                    raise err

    except Exception as err:
        errText = re.sub('[\n\r]+', ' ', errorToString(err, show_stacktrace=False))
        isBlocking = (
            'Use --list-formats' in errText
            or 'The downloaded file is empty' in errText
            # or 'fragment not found' in errText
            # or 'nsig extraction failed' in errText
        )
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = (
            "Youtube is currently blocking 3rd-party media download requests. We'll try to fix the issue ASAP."
            if isBlocking
            else 'Audio download error: ' + removeAnsiStyles(errText)
        )
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle('downloadAudioFile: Traceback for the following error:') + sTraceback)
        _logger.error(errorStyle('downloadAudioFile: ' + errMsg))
        notifyOwner('downloadAudioFile: Error: ' + errMsg, '')
        raise Exception(errMsg)
