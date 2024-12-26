# -*- coding:utf-8 -*-

from core.appConfig import TELEGRAM_OWNER_ID

#  from botCast.config.castConfig import demoVideo

from botCast.api import downloadAndSendAudioToChat

# About ~2.5h (2:25:09), Video size: ~632.1MB, Audio size: ~130Mb
largeVideoUrl = 'https://www.youtube.com/watch?v=-K2AeSsBeoo'

# About 5s, Audio size: ~22Kb
smallVideoUrl = 'https://www.youtube.com/watch?v=EngW7tLk6R8'

# ~2:47
mediumVideoUrl = 'https://www.youtube.com/watch?v=UdaQRvVTIqU'

# A video url to test
testVideo = mediumVideoUrl


def sendInfoToChatTest():
    downloadAndSendAudioToChat(
        url=testVideo,
        chatId=TELEGRAM_OWNER_ID,
        username='test',
        cleanUp=False,
    )


if __name__ == '__main__':
    try:
        sendInfoToChatTest()
    except Exception as err:
        print('ERROR:', repr(err))
