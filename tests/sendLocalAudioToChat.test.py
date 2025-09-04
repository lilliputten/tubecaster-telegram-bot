# -*- coding:utf-8 -*-

import posixpath

from botCast.helpers._sendAudioToChat import sendAudioToChat
from core.appConfig import PROJECT_PATH, TELEGRAM_OWNER_ID
from tests.testVideoInfo import videoInfo

#  audioFile = 'temp/2024-12-17-15-53-52-test/Sample Videos Dummy Videos For Demo Use.mp3'
audioFile = 'tests/test-audios/test-short.mp3'
audioFile = 'tests/test-audios/test-medium.mp3'
audioFileName = posixpath.join(PROJECT_PATH, audioFile)

maxAudioFileSize = None   # 30000


def sendLocalAudioToChat():
    sendAudioToChat(
        chatId=TELEGRAM_OWNER_ID,
        rootMessage=None,
        videoInfo=videoInfo,
        originalMessage=None,
        audioFileName=audioFileName,
        cleanUp=False,
        maxAudioFileSize=maxAudioFileSize,
    )


if __name__ == '__main__':
    try:
        sendLocalAudioToChat()
    except Exception as err:
        print('ERROR:', repr(err))
