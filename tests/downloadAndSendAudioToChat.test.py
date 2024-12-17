# -*- coding:utf-8 -*-

from core.appConfig import TELEGRAM_OWNER_ID

from bot.cast.config.castConfig import demoVideo

from bot.cast.api import downloadAndSendAudioToChat


def sendInfoToChatTest():
    downloadAndSendAudioToChat(demoVideo, TELEGRAM_OWNER_ID, 'test')


if __name__ == '__main__':
    try:
        sendInfoToChatTest()
    except Exception as err:
        print('ERROR:', repr(err))
