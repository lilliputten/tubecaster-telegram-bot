# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI
import traceback

from core.helpers.errors import errorToString
from core.helpers.time import getTimeStamp
from core.logger import getDebugLogger, titleStyle, secondaryStyle
from core.appConfig import appConfig, TELEGRAM_OWNER_ID
from core.utils import debugObj

from botApp import botApp

from botCore.helpers import getUserName


_logger = getDebugLogger()


def testCommand(chat: telebot.types.Chat, message: telebot.types.Message):
    try:
        chatId = chat.id  # Is userId
        text = message.text
        user = message.from_user
        username = chat.username
        first_name = chat.first_name
        # last_name = chat.last_name
        name = first_name if first_name else username
        json = message.json
        fromData: dict = json.get('from', {})
        languageCode = fromData.get('language_code')
        #  userId = fromData.get('id')
        if not TELEGRAM_OWNER_ID or TELEGRAM_OWNER_ID != chatId:
            botApp.reply_to(message, 'Sorry you are not allowed to use this command.')
            return
        obj = {
            'text': text,
            'timeStr': getTimeStamp(),
            'chatId': chatId,
            #  'userId': userId,
            'name': name,
            'usernameStr': getUserName(user),
            'languageCode': languageCode,
            'LOCAL': appConfig.get('LOCAL'),
            'PROJECT_INFO': appConfig.get('PROJECT_INFO'),
            'PROJECT_PATH': appConfig.get('PROJECT_PATH'),
        }
        debugStr = debugObj(obj)
        logItems = [
            titleStyle('testCommand: %s' % text),
            secondaryStyle(debugStr),
        ]
        logContent = '\n'.join(logItems)
        msgItems = [
            'Hi, %s! Here is your test results:' % name,
            debugStr,
        ]
        content = '\n\n'.join(msgItems)
        _logger.info(logContent)
        botApp.send_message(chatId, content)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'Error: ' + errText
        _logger.error('testCommand: ' + errMsg)
        print(sTraceback)
        botApp.reply_to(message, errMsg)
