import traceback

import telebot  # pyTelegramBotAPI

from botApp import botApp
from botCore.constants import emojies
from botCore.helpers import getUserName
from botCore.helpers._replyOrSend import replyOrSend
from core.appConfig import LOCAL, PROJECT_INFO, PROJECT_PATH
from core.helpers.errors import errorToString
from core.helpers.time import formatTime, getTimeStamp
from core.logger import getDebugLogger, secondaryStyle, titleStyle
from core.logger.utils import errorStyle, warningStyle
from core.utils import debugObj

_logger = getDebugLogger()

_logTraceback = False


def showOutOfLimitsMessage(message: telebot.types.Message):
    chatId = message.chat.id
    try:
        text = message.text
        sticker = message.sticker
        stickerFileId = sticker.file_id if sticker else None
        stickerEmoji = sticker.emoji if sticker else None
        stickerSetName = sticker.set_name if sticker else None
        messageId = message.id
        contentType = message.content_type
        messageDate = formatTime(None, message.date)
        user = message.from_user
        userId = user.id if user else chatId
        text = message.text
        usernameStr = getUserName(user)
        json = message.json
        fromData: dict = json.get('from', {})
        languageCode = fromData.get('language_code')
        stateValue = botApp.get_state(userId, chatId)
        commandHashItems = [
            # info,
            contentType,
            text,
        ]
        commandHash = ' '.join(filter(None, commandHashItems))
        debugItems = {
            'userId': userId,
            'commandHash': commandHash,
            'contentType': contentType,
            'messageId': messageId,
            'text': text,
            'sticker': repr(sticker),
            'stickerFileId': stickerFileId,
            'stickerSetName': stickerSetName,
            'stickerEmoji': stickerEmoji,
            'timeStr': getTimeStamp(),
            'userId': userId,
            'usernameStr': usernameStr,
            'languageCode': languageCode,
            'messageDate': messageDate,
            'stateValue': stateValue if stateValue else 'None',
            'LOCAL': LOCAL,
            'PROJECT_INFO': PROJECT_INFO,
            'PROJECT_PATH': PROJECT_PATH,
        }
        debugStr = debugObj(debugItems)
        logItems = [
            titleStyle('showOutOfLimitsMessage: %s' % commandHash),
            secondaryStyle(debugStr),
        ]
        logContent = '\n'.join(logItems)
        _logger.info(logContent)
        contentItems = [
            'Sorry, your command can not be processed.',
            'Check your /status or contact the administraor (@lilliputten) in case of any questions.',
            'You can upgrade you account with /become_user (if you are on a GUEST plan) or /get_full_access (if you want to get unlimited access) commands. See also usage /plans info.',
        ]
        replyOrSend(emojies.warning + ' ' + '\n\n'.join(contentItems), chatId, message)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error processing default command: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle(titleStyle('Traceback for the following error:') + sTraceback))
        _logger.error(errorStyle('showOutOfLimitsMessage: ' + errMsg))
        replyOrSend(emojies.robot + ' ' + errMsg, chatId, message)
