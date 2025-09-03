import traceback

import telebot  # pyTelegramBotAPI
from telebot.states.sync.context import StateContext

from botApp import botApp
from botCore.constants import emojies, stickers
from botCore.helpers import createSendRegistrationReguestButtonsMarkup, getUserName
from botCore.helpers._replyOrSend import replyOrSend
from core.appConfig import CONTROLLER_CHANNEL_ID, LOCAL, PROJECT_INFO, PROJECT_PATH
from core.helpers.errors import errorToString
from core.helpers.strings import removeAnsiStyles
from core.helpers.time import formatTime, getTimeStamp
from core.logger import getDebugLogger, secondaryStyle, titleStyle
from core.logger.utils import errorStyle, warningStyle
from core.utils import debugObj

_logger = getDebugLogger()

_logTraceback = False


def showNewUserMessage(message: telebot.types.Message, newUserId: int, newUserName: str):
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
        # fmt: off
        commandHash = ' '.join(list(filter(None, [
            # info,
            contentType,
            text,
        ])))
        # fmt: on
        debugItems = {
            'newUserId': newUserId,
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
            titleStyle('showNewUserMessage: %s' % commandHash),
            secondaryStyle(debugStr),
        ]
        logContent = '\n'.join(logItems)
        msgItems = [
            emojies.warning
            + ' Sorry, only registered users are allowed to run this command. Do you want to send a registration request?',
            # secondaryStyle(debugStr),
        ]
        content = '\n\n'.join(msgItems)
        _logger.info(logContent)
        markup = createSendRegistrationReguestButtonsMarkup(newUserId, newUserName, languageCode)
        botApp.send_message(
            chatId,
            removeAnsiStyles(content),
            reply_markup=markup,
        )
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error processing default command: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle(titleStyle('Traceback for the following error:') + sTraceback))
        _logger.error(errorStyle('showNewUserMessage: ' + errMsg))
        replyOrSend(botApp, emojies.robot + ' ' + errMsg, chatId, message)
