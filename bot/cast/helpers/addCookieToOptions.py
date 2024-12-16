# -*- coding:utf-8 -*-

import posixpath

from core.logger import getLogger
from core.appConfig import appConfig

from ..types.YtdlOptionsType import YtdlOptionsType

_logger = getLogger('bot/cast/addCookieToOptions')


def addCookieToOptions(options: YtdlOptionsType):
    destFolder = str(options.get('_destFolder', ''))

    # Use cookies (if provided):
    YT_COOKIE = appConfig.get('YT_COOKIE')
    if YT_COOKIE:
        _logger.info('addCookieToOptions: Found YT_COOKIE: %s' % '***')
        YT_COOKIE = YT_COOKIE
        cookieFile = posixpath.join(destFolder, 'cookie')  # destFile + '.cookie'
        options['cookiefile'] = cookieFile
        # Writing cookie data to a file, if it's absent...
        _logger.info('addCookieToOptions: Writing cookieFile: %s' % cookieFile)
        with open(cookieFile, 'w') as fh:
            fh.write(YT_COOKIE.strip())
