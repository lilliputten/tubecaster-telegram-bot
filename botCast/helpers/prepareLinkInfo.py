# -*- coding:utf-8 -*-

import traceback
import posixpath
import pathlib

from core.helpers.errors import errorToString
from core.helpers.files import getFileIdFromUrl, getIdFromName
from core.helpers.time import getTimeStamp
from core.logger import getLogger
from core.appConfig import AUDIO_FILE_EXT, TEMP_PATH
from core.utils import debugObj

from botCore.types import TVideoInfo

from ..config.castConfig import YTDL, logTraceback
from ..helpers.getYtdlBaseOptions import getYtdlBaseOptions

_logger = getLogger('botCast/prepareLinkInfo')


def prepareLinkInfo(url: str, username: str):
    """
    Returns local temporary saved audio file name.
    """
    try:
        _logger.info('prepareLinkInfo: Trying to get an info for the video url: %s' % url)

        # Prepare options...
        options = getYtdlBaseOptions()

        folderName = getTimeStamp('id') + '-' + username
        destFolder = options['_destFolder'] = posixpath.join(TEMP_PATH, folderName)
        # Ensure temp folder is exists
        pathlib.Path(destFolder).mkdir(parents=True, exist_ok=True)

        # DEBUG: Show options...
        # /info https://www.youtube.com/watch?v=EngW7tLk6R8
        _logger.info('prepareLinkInfo: Fetching info with options:\n%s' % debugObj(dict(options)))

        # Extract video info
        videoInfo: TVideoInfo | None = YTDL.YoutubeDL(options).extract_info(url=url, download=False)
        if not videoInfo:
            raise Exception('No video info has been returned')

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
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Prepare audio file error: ' + errText
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('prepareLinkInfo: Traceback for the following error:' + sTraceback)
        _logger.error('prepareLinkInfo: ' + errMsg)
        raise Exception(errMsg)
