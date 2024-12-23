# -*- coding:utf-8 -*-

"""
Test simple message sending code.
"""

import telebot  # pyTelegramBotAPI
import traceback

from core.logger import secondaryStyle, titleStyle
from core.utils import debugObj
from core.helpers.errors import errorToString
from core.appConfig import LOCAL, PROJECT_INFO, PROJECT_PATH, TELEGRAM_TOKEN, TELEGRAM_OWNER_ID

botApp = telebot.TeleBot(token=TELEGRAM_TOKEN, threaded=False)


def showInfo():
    obj = {
        'LOCAL': LOCAL,
        'PROJECT_INFO': PROJECT_INFO,
        'PROJECT_PATH': PROJECT_PATH,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_OWNER_ID': TELEGRAM_OWNER_ID,
    }
    debugStr = debugObj(obj)
    logItems = [
        titleStyle('testSendMessage: showInfo:'),
        secondaryStyle(debugStr),
    ]
    logContent = '\n'.join(logItems)
    print(logContent)


def sendMessage():
    botApp.send_message(TELEGRAM_OWNER_ID, 'Test')


showInfo()

try:
    print('testSendMessage: Sending test message...')
    sendMessage()
    print('testSendMessage: Message successfully sent.')
except Exception as err:
    sError = errorToString(err, show_stacktrace=False)
    sTraceback = str(traceback.format_exc())
    errMsg = 'testSendMessage: Message sending error: ' + sError
    print('testSendMessage: Traceback for the following error:' + sTraceback)
    print(errMsg)
