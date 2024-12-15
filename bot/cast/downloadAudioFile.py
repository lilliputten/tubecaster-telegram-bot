# -*- coding:utf-8 -*-

import traceback

from core.helpers.errors import errorToString
from core.logger import getLogger
from core.utils import debugObj

from .castConfig import YTDL, logTraceback
from .YtdlOptionsType import YtdlOptionsType

_logger = getLogger('bot/cast/sendInfoToChat')


def downloadAudioFile(options: YtdlOptionsType, videoInfo):
    """
    Returns local temporary saved audio file name.
    """
    try:
        webpageUrl = videoInfo.get('webpage_url')
        _logger.info('downloadAudioFile: Trying to fetch a video via the url: %s' % webpageUrl)

        destFile = options['_destFile']

        # NOTE 2024.12.10, 07:30: This code produces an error: Requested format is not available. Use --list-formats for a list of available formats
        #  addCookieToOptions(options)

        # Extend options for download:
        options = {
            **options,
            # @see https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
            'format': 'worstaudio/worst',
            #  'format': 'bestaudio/best',
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
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Audio download error: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('downloadAudioFile: Traceback for the following error:' + sTraceback)
        _logger.error('downloadAudioFile: ' + errMsg)
        raise Exception(errMsg)
