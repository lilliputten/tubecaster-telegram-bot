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
from .castCommand import castCommand, startWaitingForCastUrl, castForUrlStep
from .castTestCommand import castTestCommand
from .helpCommand import helpCommand
from .startCommand import startCommand
from .testCommand import testCommand


_logger = getDebugLogger()

_logTraceback = False


@botApp.message_handler(commands=['test'])
def testReaction(message: telebot.types.Message, state: StateContext):
    sendCommandInfo(message, 'testReaction')
    testCommand(message.chat, message, state)


@botApp.message_handler(commands=['castTest'])
def castTestReaction(message: telebot.types.Message):
    sendCommandInfo(message, 'castTestReaction')
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
        _logger.error('startCast: Error: %s' % errMsg)
        botApp.send_message(message.chat.id, errMsg)
        return
    startWaitingForCastUrl(message.chat, message)


@botApp.message_handler(state=BotStates.waitForCastUrl)
def castForUrlStepHandler(message: telebot.types.Message, state: StateContext):
    sendCommandInfo(message, 'castForUrlStepHandler')
    state.delete()
    castForUrlStep(message.chat, message)


@botApp.message_handler(commands=['cast'])
def castReaction(message: telebot.types.Message):
    sendCommandInfo(message, 'castReaction')
    castCommand(message.chat, message)


@botApp.message_handler(state=BotStates.waitForInfoUrl)
def infoForUrlStepHandler(message: telebot.types.Message, state: StateContext):
    sendCommandInfo(message, 'infoForUrlStepHandler')
    state.delete()
    infoForUrlStep(message.chat, message)


@botApp.message_handler(commands=['info'])
def infoReaction(message: telebot.types.Message, state: StateContext):
    sendCommandInfo(message, 'infoReaction')
    infoCommand(message.chat, message, state)


# Handle all other messages.
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
    try:
        contentType = message.content_type
        text = message.text

        # The command text seems to be an youtube video link, so try to cast it...
        if contentType == 'text' and text and isYoutubeLink(text):
            _logger.info(titleStyle('defaultCommand: Processing as a cast command'))
            castForUrlStep(chat, message)
        # Forcibly invoke info command if the state has been set
        elif stateValue == BotStates.waitForInfoUrl:
            _logger.info(titleStyle('defaultCommand: Forcibly invoke info command as the state has been set'))
            state.delete()
            infoForUrlStep(chat, message)
            # infoCommand(chat, message)
        # Forcibly invoke cast command if the state has been set
        elif stateValue == BotStates.waitForCastUrl:
            _logger.info(titleStyle('defaultCommand: Forcibly invoke cast command as the state has been set'))
            state.delete()
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
                + 'I didn\'t understand the command: %s\n\n' % message.text
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
            _logger.info(titleStyle('defaultCommand: Traceback for the following error:' + sTraceback))
        _logger.error('defaultCommand: ' + errMsg)
        replyOrSend(botApp, emojies.robot + ' ' + errMsg, chatId, message)


def registerCommands():
    pass
