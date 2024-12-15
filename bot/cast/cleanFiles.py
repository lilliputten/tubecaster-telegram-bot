# -*- coding:utf-8 -*-

import os
import pathlib

from .YtdlOptionsType import YtdlOptionsType


def cleanFiles(options: YtdlOptionsType):
    """
    Clean temporary files and folders created in prepareAudioFile, downloadAudioFile
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
