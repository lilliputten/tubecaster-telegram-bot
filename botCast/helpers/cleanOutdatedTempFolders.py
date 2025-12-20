# -*- coding:utf-8 -*-

import os
import re
import shutil
import traceback
from time import time

from botCommands.sendInfo import notifyOwner
from core.appConfig import TEMP_PATH
from core.helpers.errors import errorToString
from core.helpers.strings import removeAnsiStyles
from core.logger.logger import getDebugLogger
from core.logger.utils import errorStyle, primaryStyle, secondaryStyle, titleStyle, warningStyle

from ..config.castConfig import logTraceback

_logger = getDebugLogger()


def cleanOutdatedTempFolders():
    """
    Clean up all subfolders under the TEMP_PATH that are older than an hour ago with all their contents.
    """
    try:
        if not os.path.exists(TEMP_PATH):
            return  # Nothing to clean if the temp path doesn't exist
        current_time = time()
        one_hour_ago = current_time - 3600  # 3600 seconds = 1 hour
        for item in os.listdir(TEMP_PATH):
            item_path = os.path.join(TEMP_PATH, item)
            # Check if it's a directory
            if os.path.isdir(item_path):
                # Get the modification time of the directory
                dir_mtime = os.path.getmtime(item_path)
                # If the directory is older than 1 hour, remove it
                if dir_mtime < one_hour_ago:
                    _logger.info(primaryStyle('cleanOutdatedTempFolders: %s: removing...' % item))
                    try:
                        shutil.rmtree(item_path)
                        _logger.info(primaryStyle('cleanOutdatedTempFolders: %s: removed' % item))
                    except OSError as err:
                        errText = re.sub('[\n\r]+', ' ', errorToString(err, show_stacktrace=False))
                        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
                        errMsg = removeAnsiStyles(errText)
                        if logTraceback:
                            errMsg += sTraceback
                        else:
                            _logger.warning(
                                warningStyle('cleanOutdatedTempFolders: Traceback for the following error:')
                                + sTraceback
                            )
                        _logger.error(errorStyle('cleanOutdatedTempFolders: %s: remove failed' % item))
    except Exception as err:
        errText = re.sub('[\n\r]+', ' ', errorToString(err, show_stacktrace=False))
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Temp folders cleaning error: ' + removeAnsiStyles(errText)
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle('cleanOutdatedTempFolders: Traceback for the following error:') + sTraceback)
        _logger.error(errorStyle('cleanOutdatedTempFolders: ' + errMsg))
        notifyOwner('cleanOutdatedTempFolders: Error: ' + errMsg, '')
