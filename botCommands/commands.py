# -*- coding:utf-8 -*-

"""
Define all the bot commands.

See https://pytba.readthedocs.io/en/latest/sync_version/index.html
"""

import traceback
import telebot  # pyTelegramBotAPI
from telebot.states.sync.context import StateContext

from botApp.botStates import BotStates
from core.helpers.urls import isYoutubeLink
from core.logger import getDebugLogger, titleStyle, secondaryStyle
from core.helpers.errors import errorToString
from core.utils import debugObj

from botApp import botApp
from botCore.constants import stickers, emojies
from botCore.helpers import getUserName
from botCore.helpers import replyOrSend
from botCore.helpers import createCommonButtonsMarkup

from .sendInfo import sendCommandInfo, sendQueryInfo
from .infoCommand import infoCommand, infoForUrlStep
from .castCommand import castCommand
from .castTestCommand import castTestCommand
from .helpCommand import helpCommand
from .startCommand import startCommand
from .testCommand import testCommand


_logger = getDebugLogger()

_logTraceback = False


@botApp.message_handler(commands=['test'])
def testReaction(message: telebot.types.Message):
    sendCommandInfo(message)
    testCommand(message.chat, message)


@botApp.message_handler(commands=['castTest'])
def castTestReaction(message: telebot.types.Message):
    sendCommandInfo(message)
    castTestCommand(message.chat, message)


@botApp.message_handler(commands=['help'])
def helpReaction(message: telebot.types.Message):
    sendCommandInfo(message)
    helpCommand(message.chat)


@botApp.message_handler(commands=['start'])
def startReaction(message: telebot.types.Message):
    sendCommandInfo(message)
    startCommand(message.chat, message)


@botApp.callback_query_handler(lambda query: query.data == 'startHelp')
def startHelp(query: telebot.types.CallbackQuery):
    sendQueryInfo(query)
    message = query.message
    helpCommand(message.chat)


@botApp.callback_query_handler(lambda query: query.data == 'startCast')
def startCast(query: telebot.types.CallbackQuery):
    sendQueryInfo(query)
    message = query.message
    if not isinstance(message, telebot.types.Message):
        # NOTE: A normal message is required to register next step handler
        errMsg = 'Inaccessible message recieved! The message is required to register a next step handler'
        _logger.error('startCast: Error: %s' % errMsg)
        botApp.send_message(message.chat.id, errMsg)
        return
    castCommand(message.chat, message)


@botApp.message_handler(commands=['cast'])
def castReaction(message: telebot.types.Message):
    sendCommandInfo(message)
    castCommand(message.chat, message)


@botApp.message_handler(state=BotStates.waitForCastUrl)
def infoForUrlStepHandler(message: telebot.types.Message, state: StateContext):
    sendCommandInfo(message, state)
    infoForUrlStep(message.chat, message, state)


@botApp.message_handler(commands=['info'])
def infoReaction(message: telebot.types.Message, state: StateContext):
    sendCommandInfo(message, state)
    infoCommand(message.chat, message, state)


def checkDefaultCommand(message: telebot.types.Message):
    text = message.text
    sticker = message.sticker
    stickerFileId = sticker.file_id if sticker else None
    stickerEmoji = sticker.emoji if sticker else None
    stickerSetName = sticker.set_name if sticker else None
    messageId = message.id
    contentType = message.content_type
    user = message.from_user
    userId = user.id if user else None
    text = message.text
    usernameStr = getUserName(user)
    json = message.json
    fromData: dict = json.get('from', {})
    languageCode = fromData.get('language_code')
    commandHash = ' '.join(
        list(
            filter(
                None,
                [
                    contentType,
                    text,
                ],
            )
        )
    )
    obj = {
        'commandHash': commandHash,
        'contentType': contentType,
        'messageId': messageId,
        'text': text,
        'sticker': repr(sticker),
        'stickerFileId': stickerFileId,
        'stickerSetName': stickerSetName,
        'stickerEmoji': stickerEmoji,
        # 'timeStr': getTimeStamp(),
        'userId': userId,
        'usernameStr': usernameStr,
        'languageCode': languageCode,
        # 'messageDate': messageDate,
    }
    debugStr = debugObj(obj)
    logItems = [
        titleStyle('checkDefaultCommand: %s' % commandHash),
        secondaryStyle(debugStr),
    ]
    logContent = '\n'.join(logItems)
    _logger.info(logContent)
    return True


# Handle all other messages.
@botApp.message_handler(
    func=checkDefaultCommand,
    # func=lambda _: True,
    content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'],
)
def defaultCommand(message):
    sendCommandInfo(message)
    chatId = message.chat.id
    try:
        contentType = message.content_type
        text = message.text
        # The command text seems to be an youtube video link, so try to cast it...
        if contentType == 'text' and isYoutubeLink(text):
            _logger.info(titleStyle('defaultCommand: Processing as a cast command'))
            castCommand(message.chat, message)
        else:
            botApp.send_sticker(chatId, sticker=stickers.busyMrCat)
            markup = createCommonButtonsMarkup()
            botApp.send_message(
                message.chat.id,
                emojies.robot
                + " Ok, I'm here and look forward to your command.\n\nSee /help for the list of the available commands.",
                reply_markup=markup,
            )
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error processing default command: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info(titleStyle('defaultCommand: Traceback for the following error:' + sTraceback))
        _logger.error('defaultCommand: ' + errMsg)
        replyOrSend(botApp, emojies.robot + ' ' + errMsg, chatId, message)


def registerCommands():
    pass
