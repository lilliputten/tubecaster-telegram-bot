# -*- coding:utf-8 -*-

import re
import traceback

from core.helpers.errors import errorToString
from core.helpers.strings import removeAnsiStyles
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, warningStyle, secondaryStyle, primaryStyle, titleStyle
from core.utils import debugObj

from botCore.types import TVideoInfo, YtdlOptionsType

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

        # Downloading...
        with YTDL.YoutubeDL(options) as ydl:
            ydl.download([webpageUrl])  # BUG: It fails silently here for vercel serverless funciton
            # Done!
            _logger.info(
                'downloadAudioFile: Success, the audio has loaded from url %s into file %s' % (webpageUrl, destFile)
            )
            return destFile
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
