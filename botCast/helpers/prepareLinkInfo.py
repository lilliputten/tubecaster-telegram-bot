# -*- coding:utf-8 -*-

import pathlib
import posixpath
import re
import traceback
from typing import Any

from botCore.types import TVideoInfo
from core.appConfig import AUDIO_FILE_EXT, TEMP_PATH
from core.helpers.errors import errorToString
from core.helpers.files import getFileIdFromUrl, getIdFromName
from core.helpers.time import getTimeStamp
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, primaryStyle, secondaryStyle, titleStyle, warningStyle
from core.utils import debugObj

from ..config.castConfig import YTDL, logTraceback
from ..helpers.getYtdlBaseOptions import getYtdlBaseOptions

_logger = getDebugLogger()


def prepareLinkInfo(url: str, userId: int | str | None, username: str):
    """
    Returns local temporary saved audio file name.
    """
    try:
        _logger.info('prepareLinkInfo: Trying to get an info for the video url: %s' % url)

        # Prepare options...
        options = getYtdlBaseOptions()

        folderName = '-'.join(list(map(str, filter(None, [getTimeStamp('id'), str(userId), getIdFromName(username)]))))

        destFolder = options['_destFolder'] = posixpath.join(TEMP_PATH, folderName)
        # Ensure temp folder is exists
        pathlib.Path(destFolder).mkdir(parents=True, exist_ok=True)

        # DEBUG: Show options...
        # /info https://www.youtube.com/watch?v=EngW7tLk6R8
        _logger.info('prepareLinkInfo: Fetching info with options:\n%s' % debugObj(dict(options)))

        # Extract video info with format testing disabled
        info_options = {
            **options,
            'check_formats': False,  # Don't test format availability
            'format': None,  # Don't select specific format during info extraction
        }
        ytdl = YTDL.YoutubeDL(info_options)  # type: ignore
        videoInfo: TVideoInfo | None = ytdl.extract_info(url=url, download=False)   # type: ignore
        if not videoInfo:
            raise Exception('No video info has been returned')
        _logger.info('prepareLinkInfo: Got video info: %s' % debugObj(dict(videoInfo)))

        # Create file url:
        title = videoInfo.get('title')
        fileId = getIdFromName(title) if title else getFileIdFromUrl(url, username)
        filename = fileId + AUDIO_FILE_EXT
        destFile = posixpath.join(destFolder, filename)
        _logger.info('prepareLinkInfo: Computed destFile file name: %s' % destFile)

        # Set destination file name
        options['outtmpl'] = destFile
        options['_destFile'] = destFile

        return options, videoInfo
    except Exception as err:
        errText = re.sub('[\n\r]+', ' ', errorToString(err, show_stacktrace=False))
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Prepare audio file error: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle('prepareLinkInfo: Traceback for the following error:') + sTraceback)
        _logger.error(errorStyle('prepareLinkInfo: ' + errMsg))
        raise Exception(errMsg)
