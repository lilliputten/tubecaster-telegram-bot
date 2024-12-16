# -*- coding:utf-8 -*-

import telebot  # pyTelegramBotAPI

from core.logger import getLogger

from bot import botApp

from .sendInfo import sendCommandInfo, sendQueryInfo
from .infoCommand import infoCommand
from .castCommand import castCommand
from .castTestCommand import castTestCommand
from .helpCommand import helpCommand
from .startCommand import startCommand
from .testCommand import testCommand


logger = getLogger('bot/commands')


@botApp.message_handler(commands=['test'])
def testReaction(message: telebot.types.Message):
    sendCommandInfo(message)
    testCommand(message.chat, message)


@botApp.message_handler(commands=['help'])
def helpReaction(message: telebot.types.Message):
    sendCommandInfo(message)
    helpCommand(message.chat)


@botApp.message_handler(commands=['start'])
def startReaction(message: telebot.types.Message):
    sendCommandInfo(message)
    startCommand(message.chat)


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
        logger.error('startCast: Error: %s' % errMsg)
        botApp.send_message(message.chat.id, errMsg)
        return
    castCommand(message.chat, message)


@botApp.message_handler(commands=['castTest'])
def castTestReaction(message: telebot.types.Message):
    sendCommandInfo(message)
    castTestCommand(message.chat, message)


@botApp.message_handler(commands=['cast'])
def castReaction(message: telebot.types.Message):
    sendCommandInfo(message)
    castCommand(message.chat, message)


@botApp.message_handler(commands=['info'])
def infoReaction(message: telebot.types.Message):
    sendCommandInfo(message)
    infoCommand(message.chat, message)


def registerCommands():
    pass
