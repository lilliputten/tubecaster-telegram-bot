# -*- coding:utf-8 -*-

import socket
import os
import sys
import pathlib


# Inject project path to allow server-side tests
sys.path.insert(1, pathlib.Path(os.getcwd()).as_posix())


from core.appConfig import TELEGRAM_OWNER_ID
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, errorTitleStyle, warningStyle, secondaryStyle, primaryStyle, titleStyle
from core.utils import debugObj

from botCast.api import downloadAndSendAudioToChat

_logger = getDebugLogger()

# About ~2.5h (2:25:09), Video size: ~632.1MB, Audio size: ~130Mb
largeVideoUrl = 'https://www.youtube.com/watch?v=-K2AeSsBeoo'

# About 5s, Audio size: ~22Kb
smallVideoUrl = 'https://www.youtube.com/watch?v=EngW7tLk6R8'

# ~2:47
mediumVideoUrl = 'https://www.youtube.com/watch?v=UdaQRvVTIqU'

# ~0:18
mediumSmallVideoUrl = 'https://www.youtube.com/watch?v=eBHLST0pLXg'

# TEMP: Detect local developer's machine
hostname = socket.gethostname()
isLocal = hostname == 'VivoBook'

# A video url to test
testVideo = smallVideoUrl if isLocal else mediumVideoUrl


def showDebug():
    debugItems = {
        'hostname': hostname,
        'isLocal': isLocal,
        'testVideo': testVideo,
    }
    logItems = [
        titleStyle('downloadAndSendAudioToChat.test: Audio file is ready to send'),
        secondaryStyle(debugObj(debugItems)),
    ]
    logContent = '\n'.join(logItems)
    _logger.info(logContent)


def sendInfoToChatTest():
    downloadAndSendAudioToChat(
        url=testVideo,
        chatId=TELEGRAM_OWNER_ID,
        username='test',
        cleanUp=False,
    )


if __name__ == '__main__':
    try:
        showDebug()
        sendInfoToChatTest()
    except Exception as err:
        print('ERROR:', repr(err))
