# -*- coding:utf-8 -*-

import traceback

import telebot  # pyTelegramBotAPI
from telebot import types
from telebot.states.sync.context import StateContext

from botApp import botApp
from botCore.helpers import getUserName
from core.appConfig import TELEGRAM_OWNER_ID, appConfig
from core.helpers.errors import errorToString
from core.helpers.time import getTimeStamp
from core.logger import getDebugLogger, secondaryStyle, titleStyle
from core.logger.utils import errorStyle, primaryStyle, secondaryStyle, titleStyle, warningStyle
from core.utils import debugObj

_logger = getDebugLogger()

_logTraceback = False


def testCommand(chat: types.Chat, message: types.Message, _state: StateContext):
    try:
        chatId = chat.id  # Is userId
        userId = message.from_user.id if message.from_user else chatId
        stateValue = botApp.get_state(userId, chatId)
        text = message.text
        user = message.from_user
        username = chat.username
        first_name = chat.first_name
        # last_name = chat.last_name
        name = first_name if first_name else username
        json = message.json
        fromData: dict = json.get('from', {})
        languageCode = fromData.get('language_code')
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
            # 'state': state,
            'stateValue': stateValue if stateValue else 'None',
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
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle(titleStyle('testCommand: Traceback for the following error:') + sTraceback))
        _logger.error(errorStyle('testCommand: ' + errMsg))
        botApp.reply_to(message, errMsg)
