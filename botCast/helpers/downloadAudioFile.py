# -*- coding:utf-8 -*-

import re
import time
import traceback
from random import uniform

from botCore.types import TVideoInfo, YtdlOptionsType
from core.helpers.errors import errorToString
from core.helpers.strings import removeAnsiStyles
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, primaryStyle, secondaryStyle, titleStyle, warningStyle
from core.utils import debugObj

from ..config.castConfig import YTDL, logTraceback

_logger = getDebugLogger()


def downloadAudioFile(options: YtdlOptionsType, videoInfo: TVideoInfo):
    """
    Returns local temporary saved audio file name.
    """
    try:
        webpageUrl = videoInfo.get('webpage_url')
        _logger.info('downloadAudioFile: Trying to fetch a video via the url: %s' % webpageUrl)

        destFile = options.get('_destFile')
        if not destFile:
            raise ValueError("'_destFile' option is required")

        # NOTE 2024.12.10, 07:30: This code produces an error: Requested format is not available. Use --list-formats for a list of available formats
        #  addCookieToOptions(options)

        # Extend options for download:
        # TODO: Analyze videoInfo['formats'] (got with `listformats` option, see an example in `tests/yt-dlp-listformats.py`, and related artifacts)
        options = {
            **options,
            # @see https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
            # 'format': 'worstaudio/worst',
            # 'format': 'bestaudio/best',
            'format': 'bestaudio[format_note*=original]/bestaudio',  # Trying to get an original audio track
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

        # # Downloading (old version: a single attempt)...
        # with YTDL.YoutubeDL(options) as ydl:   # type: ignore
        #     ydl.download([webpageUrl])   # type: ignore
        #     # Done!
        #     _logger.info(
        #         'downloadAudioFile: Success, the audio has loaded from url %s into file %s' % (webpageUrl, destFile)
        #     )
        #     return destFile

        # Downloading with retry logic for YouTube's anti-bot patterns...
        max_retries = 5  # Increased to handle typical YouTube blocking patterns
        for attempt in range(max_retries):
            try:
                with YTDL.YoutubeDL(options) as ydl:   # type: ignore
                    ydl.download([webpageUrl])   # type: ignore
                    # Done!
                    _logger.info(
                        'downloadAudioFile: Success, the audio has loaded from url %s into file %s (attempt %d)'
                        % (webpageUrl, destFile, attempt + 1)
                    )
                    return destFile
            except Exception as retry_err:
                is_403_error = '403' in str(retry_err) or 'Forbidden' in str(retry_err)
                is_retryable = is_403_error or 'HTTP Error' in str(retry_err)

                if is_retryable and attempt < max_retries - 1:
                    # Use longer delays for YouTube's rate limiting patterns
                    base_delay = 3 + (attempt * 2)  # 3s, 5s, 7s, 9s
                    wait_time = base_delay + uniform(0, 2)  # Add jitter
                    _logger.warning(
                        f'downloadAudioFile: Attempt {attempt + 1} failed ({str(retry_err)[:100]}...), retrying in {wait_time:.1f}s'
                    )
                    time.sleep(wait_time)
                    continue
                else:
                    # Re-raise the exception if not retryable or exhausted retries
                    raise retry_err

    except Exception as err:
        errText = re.sub('[\n\r]+', ' ', errorToString(err, show_stacktrace=False))
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Audio download error: ' + removeAnsiStyles(errText)
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle('downloadAudioFile: Traceback for the following error:') + sTraceback)
        _logger.error(errorStyle('downloadAudioFile: ' + errMsg))
        raise Exception(errMsg)
