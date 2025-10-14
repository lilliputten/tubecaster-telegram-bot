# -*- coding:utf-8 -*-

from botCore.types import YtdlOptionsType
from core.appConfig import TEMP_PATH, appConfig
from core.logger import getDebugLogger, secondaryStyle, titleStyle

_logger = getDebugLogger()


def getYtdlBaseOptions():
    # Prepare options:
    options: YtdlOptionsType = {
        # @see https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
        'verbose': True,
        'cachedir': TEMP_PATH,
        'paths': {
            'temp': TEMP_PATH,
        },
        'verbose': True,
        'noplaylist': True,
        'keepvideo': False,
        'extractor_args': None,
        'outtmpl': None,
        '_destFolder': None,
        '_destFile': None,
        'cookiefile': None,
        'format': None,
        # 'listformats': True,
        #  'debug_printtraffic': None,
    }

    # Add PO Token (if exists), see https://github.com/yt-dlp/yt-dlp/wiki/Extractors#manually-acquiring-a-po-token-from-a-browser-for-use-when-logged-out
    YT_POTOKEN = appConfig.get('YT_POTOKEN')
    if YT_POTOKEN:
        _logger.info('getYtdlBaseOptions: Using YT_POTOKEN: %s' % (YT_POTOKEN))
        options['extractor_args'] = {'youtube': {'player-client': ['web'], 'po_token': ['web+' + YT_POTOKEN]}}

    #  # Add authentication params (NOTE: Unused as not supported)
    #  YT_USERNAME = appConfig.get('YT_USERNAME')
    #  YT_PASSWORD = appConfig.get('YT_PASSWORD')
    #  if YT_USERNAME and YT_PASSWORD:
    #      _logger.info('getYtdlBaseOptions: Using username (%s) and password (***)' % (YT_USERNAME))
    #      options['username'] = YT_USERNAME
    #      options['password'] = YT_PASSWORD

    return options
