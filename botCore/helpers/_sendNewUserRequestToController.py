import traceback

import telebot  # pyTelegramBotAPI
from telebot.states.sync.context import StateContext

from botApp import botApp
from botApp.botStates import BotStates
from botCore.constants import emojies
from botCore.helpers import createAcceptNewUserButtonsMarkup, getUserName
from botCore.helpers._replyOrSend import replyOrSend
from core.appConfig import CONTROLLER_CHANNEL_ID, LOCAL, LOGGING_CHANNEL_ID, PROJECT_INFO, PROJECT_PATH
from core.helpers.errors import errorToString
from core.helpers.time import formatTime, getTimeStamp
from core.logger import getDebugLogger, secondaryStyle, titleStyle
from core.logger.utils import errorStyle, warningStyle
from core.utils import debugObj

_logger = getDebugLogger()

_logTraceback = False


def sendNewUserRequestToController(
    message: telebot.types.Message, newUserId: int, newUserStr: str, state: StateContext
):
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
            contentType,
            text,
        ])))
        # fmt: on
        debugItems = {
            'CONTROLLER_CHANNEL_ID': CONTROLLER_CHANNEL_ID,
            'LOGGING_CHANNEL_ID': LOGGING_CHANNEL_ID,
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
            titleStyle('sendNewUserRequestToController: %s' % commandHash),
            secondaryStyle(debugStr),
        ]
        logContent = '\n'.join(logItems)
        contentItems = [
            emojies.question
            + f' A new user has requested registration: {newUserStr}, id {newUserId}, tg://user?id={newUserId}, language: {languageCode}',
            # secondaryStyle(debugStr),
        ]
        content = '\n\n'.join(contentItems)
        _logger.info(logContent)
        markup = createAcceptNewUserButtonsMarkup(newUserId, newUserStr, languageCode)
        botApp.send_message(
            CONTROLLER_CHANNEL_ID,
            content,
            reply_markup=markup,
        )
        botApp.send_message(
            newUserId,
            emojies.success
            + ' '
            + '\n\n'.join(
                [
                    "YOU'VE JUST REQUESTED A FREE MEMBEERSHIP.",
                    "Your request will be reviewed soon. You'll receive a notification if it is accepted.",
                    'But, it would be very helpful if you sent a brief information about yourself and why you decided to use this bot. Contact the administrator via @lilliputten in this case.',
                    'There are a lot of spam requests and we are trying to accept real and motivated humans for the free tier.',
                    'Alternatively, you can obtain a paid usbcription via /get_full_access command.',
                    'See /plans for the detailed information on all the available plans',
                    'Thanks for understanding.',
                    'Now please enter the message below if you wish (or enter /no otherwise):',
                ]
            ),
        )
        state.set(BotStates.waitForRegistrationInfo)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error processing default command: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle(titleStyle('Traceback for the following error:') + sTraceback))
        _logger.error(errorStyle('sendNewUserRequestToController: ' + errMsg))
        replyOrSend(botApp, emojies.robot + ' ' + errMsg, chatId, message)
