# -*- coding:utf-8 -*-

"""
Define all the bot commands.

See https://pytba.readthedocs.io/en/latest/sync_version/index.html
"""

import traceback
import telebot  # pyTelegramBotAPI
from telebot.states.sync.context import StateContext

from core.appConfig import LOGGING_CHANNEL_ID, TELEGRAM_OWNER_ID
from core.helpers.time import formatTime
from core.helpers.urls import isYoutubeLink
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, warningStyle, secondaryStyle, primaryStyle, titleStyle
from core.helpers.errors import errorToString
from core.utils import debugObj

from botCore.constants import stickers, emojies
from botCore.helpers import addNewValidUser
from botCore.helpers import checkValidUser, getUserName
from botCore.helpers import replyOrSend
from botCore.helpers import createCommonButtonsMarkup
from botCore.helpers import showNewUserMessage, sendNewUserRequestToController

from botApp import botApp
from botApp.botStates import BotStates

from .sendInfo import sendCommandInfo, sendQueryInfo
from .infoCommand import infoCommand, infoForUrlStep
from .castCommand import castCommand, startWaitingForCastUrl, castForUrlStep
from .castTestCommand import castTestCommand
from .helpCommand import helpCommand
from .startCommand import startCommand
from .testCommand import testCommand


_logger = getDebugLogger()

_logTraceback = False


@botApp.message_handler(commands=['register'])
def requestRegistration(message: telebot.types.Message):
    sendCommandInfo(message, 'requestRegistration')
    newUserId = message.from_user.id if message.from_user else message.chat.id
    newUserStr = getUserName(message.from_user)
    sendNewUserRequestToController(message, newUserId, newUserStr)


@botApp.callback_query_handler(lambda query: query.data.startswith('registerUser:'))
def registerUserQuery(query: telebot.types.CallbackQuery):
    sendQueryInfo(query, query.data)
    message = query.message
    if not isinstance(message, telebot.types.Message):
        # NOTE: A normal message is required to register next step handler
        errMsg = 'Inaccessible message recieved! The message is required to register a next step handler'
        _logger.error(errorStyle('registerUserQuery: Error: %s' % errMsg))
        botApp.send_message(message.chat.id, errMsg)
        return
    if query.data is not None:
        list = query.data.split(':')
        newUserId = int(list[1])
        newUserStr = str(list[2])
        sendNewUserRequestToController(message, newUserId, newUserStr)


@botApp.callback_query_handler(lambda query: query.data.startswith('acceptUser:'))
def acceptUserQuery(query: telebot.types.CallbackQuery):
    sendQueryInfo(query, query.data)
    if query.data is not None:
        list = query.data.split(':')
        newUserId = int(list[1])
        newUserStr = str(list[2])
        addNewValidUser(newUserId, newUserStr, query)
        botApp.send_message(
            newUserId, emojies.success + " You've been successfully added to the registered users list!"
        )
        message = query.message
        if isinstance(message, telebot.types.Message):
            newUserName = getUserName(query.from_user)
            botApp.reply_to(message, emojies.success + f' User request from {newUserName} has been accepted')


@botApp.callback_query_handler(lambda query: query.data.startswith('rejectUser:'))
def rejectUserQuery(query: telebot.types.CallbackQuery):
    sendQueryInfo(query, query.data)
    if query.data is not None:
        list = query.data.split(':')
        newUserId = int(list[1])
        botApp.send_message(
            newUserId,
            emojies.error
            + ' Unfortunatelly, your registration has been declined. You can try again or better reach the administrator (@lilliputten).',
        )
        message = query.message
        if isinstance(message, telebot.types.Message):
            newUserName = getUserName(query.from_user)
            botApp.reply_to(message, emojies.error + f' User request from {newUserName} has been rejected.')


@botApp.message_handler(commands=['test'])
def testReaction(message: telebot.types.Message, state: StateContext):
    # DEBUG
    sendCommandInfo(message, 'testReaction')
    userId = message.from_user.id if message.from_user else message.chat.id
    if userId != TELEGRAM_OWNER_ID:
        replyOrSend(botApp, emojies.error + ' The command is not allowed!', message.chat.id, message)
    else:
        testCommand(message.chat, message, state)


@botApp.message_handler(commands=['castTest'])
def castTestReaction(message: telebot.types.Message):
    sendCommandInfo(message, 'castTestReaction')
    userId = message.from_user.id if message.from_user else message.chat.id
    if userId != TELEGRAM_OWNER_ID:
        replyOrSend(botApp, emojies.error + ' The command is not allowed!', message.chat.id, message)
    else:
        castTestCommand(message.chat, message)


@botApp.message_handler(commands=['help'])
def helpReaction(message: telebot.types.Message):
    sendCommandInfo(message, 'helpReaction')
    helpCommand(message.chat)


@botApp.message_handler(commands=['start'])
def startReaction(message: telebot.types.Message):
    sendCommandInfo(message, 'startReaction')
    startCommand(message.chat, message)


@botApp.callback_query_handler(lambda query: query.data == 'startHelp')
def startHelp(query: telebot.types.CallbackQuery):
    sendQueryInfo(query, 'startHelp')
    message = query.message
    helpCommand(message.chat)


@botApp.callback_query_handler(lambda query: query.data == 'startCast')
def startCast(query: telebot.types.CallbackQuery):
    sendQueryInfo(query, 'startCast')
    message = query.message
    if not isinstance(message, telebot.types.Message):
        # NOTE: A normal message is required to register next step handler
        errMsg = 'Inaccessible message recieved! The message is required to register a next step handler'
        _logger.error(errorStyle('startCast: Error: %s' % errMsg))
        botApp.send_message(message.chat.id, errMsg)
        return
    userId = query.from_user.id if query.from_user else message.chat.id
    if not checkValidUser(userId):
        newUserName = getUserName(query.from_user)
        _logger.info(titleStyle(f'Invalid user: {newUserName} ({userId})'))
        showNewUserMessage(message, userId, newUserName)
    else:
        startWaitingForCastUrl(message.chat, message)


@botApp.message_handler(state=BotStates.waitForCastUrl)
def castForUrlStepHandler(message: telebot.types.Message, state: StateContext):
    sendCommandInfo(message, 'castForUrlStepHandler')
    state.delete()
    castForUrlStep(message.chat, message)


@botApp.message_handler(commands=['cast'])
def castReaction(message: telebot.types.Message):
    sendCommandInfo(message, 'castReaction')
    userId = message.from_user.id if message.from_user else message.chat.id
    if not checkValidUser(userId):
        newUserName = getUserName(message.from_user)
        _logger.info(titleStyle(f'Invalid user: {newUserName} ({userId})'))
        showNewUserMessage(message, userId, newUserName)
    else:
        castCommand(message.chat, message)


@botApp.message_handler(state=BotStates.waitForInfoUrl)
def infoForUrlStepHandler(message: telebot.types.Message, state: StateContext):
    sendCommandInfo(message, 'infoForUrlStepHandler')
    state.delete()
    infoForUrlStep(message.chat, message)


@botApp.message_handler(commands=['info'])
def infoReaction(message: telebot.types.Message, state: StateContext):
    sendCommandInfo(message, f'infoReaction')
    userId = message.from_user.id if message.from_user else message.chat.id
    if not checkValidUser(userId):
        newUserName = getUserName(message.from_user)
        _logger.info(titleStyle(f'Invalid user: {newUserName} ({userId})'))
        showNewUserMessage(message, userId, newUserName)
    else:
        infoCommand(message.chat, message, state)


# Handle all other messages
@botApp.message_handler(
    # func=checkDefaultCommand,
    func=lambda _: True,
    content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'],
    state=None,
)
def defaultCommand(message: telebot.types.Message, state: StateContext):
    sendCommandInfo(message, 'defaultCommand')
    chat = message.chat
    chatId = chat.id
    stateValue = state.get()
    userId = message.from_user.id if message.from_user else message.chat.id
    try:
        contentType = message.content_type
        text = message.text

        # The command text seems to be an youtube video link, so try to cast it...
        if contentType == 'text' and text and isYoutubeLink(text):
            _logger.info(titleStyle('defaultCommand: Processing as a cast command'))
            if not checkValidUser(userId):
                newUserName = getUserName(message.from_user)
                _logger.info(titleStyle(f'Invalid user: {newUserName} ({userId})'))
                showNewUserMessage(message, userId, newUserName)
            else:
                castForUrlStep(chat, message)
        # Forcibly invoke info command if the state has been set
        elif stateValue == BotStates.waitForInfoUrl:
            _logger.info(titleStyle('defaultCommand: Forcibly invoke info command as the state has been set'))
            state.delete()
            if not checkValidUser(userId):
                newUserName = getUserName(message.from_user)
                _logger.info(titleStyle(f'Invalid user: {newUserName} ({userId})'))
                showNewUserMessage(message, userId, newUserName)
            else:
                infoForUrlStep(chat, message)
                # infoCommand(chat, message)
        # Forcibly invoke cast command if the state has been set
        elif stateValue == BotStates.waitForCastUrl:
            _logger.info(titleStyle('defaultCommand: Forcibly invoke cast command as the state has been set'))
            state.delete()
            if not checkValidUser(userId):
                newUserName = getUserName(message.from_user)
                _logger.info(titleStyle(f'Invalid user: {newUserName} ({userId})'))
                showNewUserMessage(message, userId, newUserName)
            else:
                castForUrlStep(chat, message)
                # castCommand(chat, message)
        # Else show a perplexing message
        else:
            _logger.info(titleStyle('defaultCommand: Show a perplexing message'))
            botApp.send_sticker(chatId, sticker=stickers.busyMrCat)
            markup = createCommonButtonsMarkup()
            botApp.send_message(
                message.chat.id,
                emojies.question
                + ' '
                + "I didn't understand the command: %s\n\n" % message.text
                + "But I'm still here and look forward to your next command.\n\n"
                + 'See /help for the reference of all the available commands.',
                reply_markup=markup,
            )
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error processing default command: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle(titleStyle('defaultCommand: Traceback for the following error:') + sTraceback))
        _logger.error(errorStyle('defaultCommand: ' + errMsg))
        replyOrSend(botApp, emojies.robot + ' ' + errMsg, chatId, message)


def registerCommands():
    botApp.load_next_step_handlers()
