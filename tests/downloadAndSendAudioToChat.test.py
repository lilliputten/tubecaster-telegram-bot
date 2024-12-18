# -*- coding:utf-8 -*-

from core.appConfig import TELEGRAM_OWNER_ID

#  from botCast.config.castConfig import demoVideo

from botCast.api import downloadAndSendAudioToChat

# About ~2.5h (2:25:09), Video size: ~632.1MB, Audio size: ~130Mb
largeVideoUrl = 'https://www.youtube.com/watch?v=-K2AeSsBeoo'

# About 5s, Audio size: ~22Kb
smallVideoUrl = 'https://www.youtube.com/watch?v=EngW7tLk6R8'


def sendInfoToChatTest():
    downloadAndSendAudioToChat(
        smallVideoUrl,
        TELEGRAM_OWNER_ID,
        'test',
    )


if __name__ == '__main__':
    try:
        sendInfoToChatTest()
    except Exception as err:
        print('ERROR:', repr(err))
