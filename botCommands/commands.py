# -*- coding:utf-8 -*-

"""
Define all the bot commands.

See https://pytba.readthedocs.io/en/latest/sync_version/index.html
"""

import traceback
from datetime import datetime

# import telebot  # pyTelegramBotAPI
from telebot import types
from telebot.states.sync.context import StateContext

from botApp import botApp
from botApp.botStates import BotStates
from botCore.constants import emojies, stickers
from botCore.helpers import (
    addNewValidUser,
    createCommonButtonsMarkup,
    getUserName,
    replyOrSend,
    sendNewUserRequestToController,
)
from botCore.helpers.plans import getPlansInfoMessage
from botCore.helpers.status import checkUserLimitations, getUserStatusShortSummaryInfoMessage, showOutOfLimitsMessage
from core.appConfig import CONTROLLER_CHANNEL_ID, TELEGRAM_OWNER_ID
from core.helpers.errors import errorToString
from core.helpers.urls import isYoutubeLink
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, primaryStyle, secondaryStyle, titleStyle, warningStyle
from core.utils import debugObj
from db import initDb

from .castCommand import castCommand, castForUrlStep, startWaitingForCastUrl
from .castTestCommand import castTestCommand
from .helpCommand import helpCommand
from .infoCommand import infoCommand, infoForUrlStep
from .requestFullAccess import requestFullAccess
from .requestFullAccessPayment import requestFullAccessPayment  # Import to register payment handlers
from .sendInfo import sendCommandInfo, sendQueryInfo
from .showRemoveAccountDialog import showRemoveAccountDialog
from .startCommand import startCommand
from .statsCommand import statsCommand
from .testCommand import testCommand

_logger = getDebugLogger()

_logTraceback = False

# List some externally registered handlers
__all__ = [
    'requestFullAccess',
    'requestFullAccessPayment',
]


@botApp.message_handler(commands=['become_user'])
def requestRegistration(message: types.Message, state: StateContext):
    sendCommandInfo(message, 'requestRegistration')
    userId = message.from_user.id if message.from_user else message.chat.id
    userStr = getUserName(message.from_user)
    sendNewUserRequestToController(message, userId, userStr, state)


@botApp.callback_query_handler(lambda query: query.data.startswith('registerUser:'))
def registerUserQuery(query: types.CallbackQuery, state: StateContext):
    sendQueryInfo(query, query.data)
    message = query.message
    if not isinstance(message, types.Message):
        # NOTE: A normal message is required to register next step handler
        errMsg = 'Inaccessible message recieved! The message is required to register a next step handler'
        _logger.error(errorStyle('registerUserQuery: Error: %s' % errMsg))
        botApp.send_message(message.chat.id, errMsg)
        return
    if query.data is not None:
        list = query.data.split(':')
        userId = int(list[1])
        userStr = str(list[2])
        sendNewUserRequestToController(message, userId, userStr, state)


@botApp.message_handler(state=BotStates.waitForRegistrationInfo)
def sendRegistrationInfoStep(message: types.Message, state: StateContext):
    sendCommandInfo(message, 'sendRegistrationInfoStep')
    state.delete()
    chat = message.chat
    text = message.text
    chatId = chat.id
    userId = message.from_user.id if message.from_user else message.chat.id
    username = getUserName(message.from_user, True)
    if not text:
        botApp.reply_to(message, 'Message text or /no is expected.')
        return
    if text == '/no':
        botApp.reply_to(
            message, emojies.success + ' Ok, you can always drop a line to the administrator (@lilliputten), anytime.'
        )
        return
    obj = {
        'text': text,
        'chatId': chatId,
        'userId': userId,
        'username': username,
    }
    debugStr = debugObj(obj)
    logItems = [
        titleStyle('sendRegistrationInfoStep'),
        secondaryStyle(debugStr),
    ]
    _logger.info('\n'.join(logItems))
    contentItems = [
        emojies.memo + f' The user {username} sent a registration message:',
        text,
    ]
    content = '\n\n'.join(contentItems)
    botApp.send_message(
        CONTROLLER_CHANNEL_ID,
        content,
    )
    botApp.reply_to(
        message,
        emojies.success
        + ' '
        + '\n\n'.join(
            [
                'YOUR MESSAGE HAS BEEN SENT TO THE ADMINISTRATOR.',
                'This should speed up the registration process.',
                'If there is no response for a long time, you can request the reqistration again (via /become_user command), or (better) drop a message to the administrator (@lilliputten).',
                'Or, alternatively, you can obtain a paid subcription via the /get_full_access command. See the usage /plans details for more information.',
            ]
        ),
    )


@botApp.callback_query_handler(lambda query: query.data.startswith('acceptUser:'))
def acceptUserQuery(query: types.CallbackQuery):
    """
    Creation of the user when it has been accepted by the admin
    """
    sendQueryInfo(query, query.data)
    if query.data is not None:
        list = query.data.split(':')
        userId = int(list[1])
        userStr = str(list[2])
        languageCode = str(list[3])
        addNewValidUser(userId, userStr, languageCode, query)
        contentItems = [
            "YOU'VE BEEN SUCCESSFULLY ADDED TO THE REGISTERED USERS LIST!",
            getUserStatusShortSummaryInfoMessage(userId),
        ]
        botApp.send_message(userId, emojies.success + ' ' + '\n\n'.join(filter(None, contentItems)))
        message = query.message
        if isinstance(message, types.Message):
            botApp.reply_to(
                message,
                emojies.success
                + f' User request from {userStr} has been accepted. Id: {userId}, tg://user?id={userId}',
            )


@botApp.callback_query_handler(lambda query: query.data.startswith('rejectUser:'))
def rejectUserQuery(query: types.CallbackQuery):
    """
    Rejection of the user when it has been accepted by the admin
    """
    sendQueryInfo(query, query.data)
    if query.data is not None:
        list = query.data.split(':')
        userId = int(list[1])
        userStr = str(list[2])
        botApp.send_message(
            userId,
            emojies.error
            + ' Unfortunatelly, your registration has been declined. You can try again or better reach the administrator (@lilliputten).',
        )
        message = query.message
        if isinstance(message, types.Message):
            botApp.reply_to(
                message,
                emojies.error + f' User request from {userStr} has been rejected. Id: {userId}, tg://user?id={userId}',
            )


@botApp.message_handler(commands=['restore_account'])
def restoreAccount(message: types.Message):
    sendCommandInfo(message, 'restoreAccount')
    userId = message.from_user.id if message.from_user else message.chat.id
    prisma = initDb()
    try:
        user = prisma.user.find_first(where={'id': userId, 'isDeleted': True})
        if not user:
            botApp.reply_to(
                message,
                emojies.error + ' ' + 'No such deleted account found.'
                " You either don't have an account at all yet, or it's not deleted.",
            )
            return
        prisma.user.update(where={'id': userId}, data={'isDeleted': False})
        contentItems = [
            'Your account has been already restored.',
        ]
        botApp.reply_to(message, emojies.success + ' ' + '\n\n'.join(filter(None, contentItems)))
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error deleting user: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle(titleStyle('Traceback for the following error:') + sTraceback))
        _logger.error(errorStyle('restoreAccount: ' + errMsg))
        botApp.reply_to(message, emojies.error + ' ' + errMsg)


@botApp.message_handler(commands=['remove_account'])
def removeAccount(message: types.Message):
    sendCommandInfo(message, 'removeAccount')
    showRemoveAccountDialog(message)


@botApp.callback_query_handler(lambda query: query.data == 'removeAccountYes')
def removeAccountYes(query: types.CallbackQuery):
    sendQueryInfo(query, 'removeAccountYes')
    message = query.message
    if not isinstance(message, types.Message):
        # NOTE: A normal message is required to register next step handler
        errMsg = 'Inaccessible message recieved!'
        _logger.error(errorStyle('removeAccountYes: Error: %s' % errMsg))
        botApp.send_message(message.chat.id, emojies.error + ' ' + errMsg)
        return
    userId = query.from_user.id if query.from_user else message.chat.id
    prisma = initDb()
    try:
        user = prisma.user.find_first(where={'id': userId, 'isDeleted': False})
        if not user or user.isDeleted:
            botApp.reply_to(message, emojies.error + ' ' + 'No such account found!')
            return
        prisma.user.update(where={'id': userId}, data={'isDeleted': True, 'deletedAt': datetime.now()})
        contentItems = [
            'Your account has been marked to deletion and will be completely wiped out in a month.',
            'You can restore the account during this time via /restore_account command.',
        ]
        botApp.reply_to(message, emojies.success + ' ' + '\n\n'.join(filter(None, contentItems)))
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error deleting user: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle(titleStyle('Traceback for the following error:') + sTraceback))
        _logger.error(errorStyle('removeAccountYes: ' + errMsg))
        botApp.reply_to(message, emojies.error + ' ' + errMsg)


@botApp.callback_query_handler(lambda query: query.data == 'removeAccountNo')
def removeAccountNo(query: types.CallbackQuery):
    sendQueryInfo(query, 'removeAccountNo')
    message = query.message
    if isinstance(message, types.Message):
        botApp.delete_message(message.chat.id, message.id)


@botApp.message_handler(commands=['test'])
def testReaction(message: types.Message, state: StateContext):
    # DEBUG
    sendCommandInfo(message, 'testReaction')
    userId = message.from_user.id if message.from_user else message.chat.id
    if userId != TELEGRAM_OWNER_ID:
        replyOrSend(emojies.error + ' The command is not allowed!', message.chat.id, message)
    else:
        testCommand(message.chat, message, state)


@botApp.message_handler(commands=['cast_test'])
def castTestReaction(message: types.Message):
    sendCommandInfo(message, 'castTestReaction')
    userId = message.from_user.id if message.from_user else message.chat.id
    if userId != TELEGRAM_OWNER_ID:
        replyOrSend(emojies.error + ' The command is not allowed!', message.chat.id, message)
    else:
        castTestCommand(message.chat, message)


@botApp.message_handler(commands=['help'])
def helpReaction(message: types.Message):
    sendCommandInfo(message, 'helpReaction')
    helpCommand(message.chat)


@botApp.message_handler(commands=['start'])
def startReaction(message: types.Message):
    sendCommandInfo(message, 'startReaction')
    startCommand(message.chat, message)


@botApp.callback_query_handler(lambda query: query.data == 'startHelp')
def startHelp(query: types.CallbackQuery):
    sendQueryInfo(query, 'startHelp')
    message = query.message
    helpCommand(message.chat)


@botApp.callback_query_handler(lambda query: query.data == 'startCast')
def startCast(query: types.CallbackQuery):
    sendQueryInfo(query, 'startCast')
    message = query.message
    if not isinstance(message, types.Message):
        # NOTE: A normal message is required to register next step handler
        errMsg = 'Inaccessible message recieved! The message is required to register a next step handler'
        _logger.error(errorStyle('startCast: Error: %s' % errMsg))
        botApp.send_message(message.chat.id, errMsg)
        return
    userId = query.from_user.id if query.from_user else message.chat.id
    # if not checkValidUser(userId):
    #     newUserName = getUserName(query.from_user)
    #     _logger.info(titleStyle(f'Invalid user: {newUserName} ({userId})'))
    #     showNewUserMessage(message, userId, newUserName)
    if not checkUserLimitations(message, userId, 'CAST'):
        showOutOfLimitsMessage(message)
    else:
        startWaitingForCastUrl(message.chat, message)


@botApp.message_handler(state=BotStates.waitForCastUrl)
def castForUrlStepHandler(message: types.Message, state: StateContext):
    sendCommandInfo(message, 'castForUrlStepHandler')
    state.delete()
    castForUrlStep(message.chat, message)


@botApp.message_handler(commands=['cast'])
def castReaction(message: types.Message):
    sendCommandInfo(message, 'castReaction')
    userId = message.from_user.id if message.from_user else message.chat.id
    if not checkUserLimitations(message, userId, 'CAST'):
        showOutOfLimitsMessage(message)
    else:
        castCommand(message.chat, message)


@botApp.message_handler(state=BotStates.waitForInfoUrl)
def infoForUrlStepHandler(message: types.Message, state: StateContext):
    sendCommandInfo(message, 'infoForUrlStepHandler')
    state.delete()
    infoForUrlStep(message.chat, message)


@botApp.message_handler(commands=['info'])
def infoReaction(message: types.Message, state: StateContext):
    sendCommandInfo(message, f'infoReaction')
    userId = message.from_user.id if message.from_user else message.chat.id
    # if not checkValidUser(userId):
    #     newUserName = getUserName(message.from_user)
    #     _logger.info(titleStyle(f'Invalid user: {newUserName} ({userId})'))
    #     showNewUserMessage(message, userId, newUserName)
    if not checkUserLimitations(message, userId, 'INFO'):
        showOutOfLimitsMessage(message)
    else:
        infoCommand(message.chat, message, state)


@botApp.message_handler(commands=['stats'])
def statsReaction(message: types.Message, state: StateContext):
    sendCommandInfo(message, f'statsReaction')
    statsCommand(message.chat, message, state)


@botApp.message_handler(commands=['status'])
def statusReaction(message: types.Message):
    sendCommandInfo(message, f'statusReaction')
    userId = message.from_user.id if message.from_user else message.chat.id
    # user = getActiveUser(userId)
    # userStr = getUserName(message.from_user)
    content = getUserStatusShortSummaryInfoMessage(userId)
    botApp.reply_to(
        message,
        emojies.info + ' ' + content,
        # parse_mode='Markdown',
    )


@botApp.message_handler(commands=['plans'])
def plansReaction(message: types.Message):
    sendCommandInfo(message, f'plansReaction')
    userId = message.from_user.id if message.from_user else message.chat.id
    # userStr = getUserName(message.from_user)
    content = getPlansInfoMessage(userId)
    botApp.reply_to(
        message,
        emojies.info + ' ' + content,
        # parse_mode='Markdown',
    )


# Handle all other messages
@botApp.message_handler(
    # func=checkDefaultCommand,
    func=lambda _: True,
    content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'],
    state=None,
)
def defaultCommand(message: types.Message, state: StateContext):
    sendCommandInfo(message, 'defaultCommand')
    chat = message.chat
    chatId = chat.id
    stateValue = state.get()
    userId = message.from_user.id if message.from_user else message.chat.id
    contentType = message.content_type
    text = message.text
    try:
        # Check states and default commands...

        # Forcibly invoke info command if the state has been set
        if stateValue == BotStates.waitForRegistrationInfo:
            _logger.info(titleStyle('defaultCommand: Forcibly invoke registration message sending'))
            sendRegistrationInfoStep(message, state)
        # Forcibly invoke info command if the state has been set
        elif stateValue == BotStates.waitForInfoUrl:
            _logger.info(titleStyle('defaultCommand: Forcibly invoke info command as the state has been set'))
            state.delete()
            # if not checkValidUser(userId):
            #     newUserName = getUserName(message.from_user)
            #     _logger.info(titleStyle(f'Invalid user: {newUserName} ({userId})'))
            #     showNewUserMessage(message, userId, newUserName)
            if not checkUserLimitations(message, userId, 'INFO'):
                showOutOfLimitsMessage(message)
            else:
                infoForUrlStep(chat, message)
        # Forcibly invoke cast command if the state has been set
        elif stateValue == BotStates.waitForCastUrl:
            _logger.info(titleStyle('defaultCommand: Forcibly invoke cast command as the state has been set'))
            state.delete()
            # if not checkValidUser(userId):
            #     newUserName = getUserName(message.from_user)
            #     _logger.info(titleStyle(f'Invalid user: {newUserName} ({userId})'))
            #     showNewUserMessage(message, userId, newUserName)
            if not checkUserLimitations(message, userId, 'CAST'):
                showOutOfLimitsMessage(message)
            else:
                castForUrlStep(chat, message)
        # The command text seems to be an youtube video link, so try to cast it...
        elif contentType == 'text' and text and isYoutubeLink(text):
            _logger.info(titleStyle('defaultCommand: Processing as a cast command'))
            # if not checkValidUser(userId):
            #     newUserName = getUserName(message.from_user)
            #     _logger.info(titleStyle(f'Invalid user: {newUserName} ({userId})'))
            #     showNewUserMessage(message, userId, newUserName)
            if not checkUserLimitations(message, userId, 'CAST'):
                showOutOfLimitsMessage(message)
            else:
                castForUrlStep(chat, message)
        # Else show a perplexing message
        else:
            _logger.info(titleStyle('defaultCommand: Show a perplexing message'))
            botApp.send_sticker(chatId, sticker=stickers.busyMrCat)
            markup = createCommonButtonsMarkup()
            botApp.send_message(
                message.chat.id,
                emojies.hmm
                + ' '
                + '\n\n'.join(
                    [
                        "I didn't understand the command: %s" % message.text,
                        "But I'm still here and look forward to your next command.",
                        'Just post a YouTube url or enter one of the available commands.',
                        'See /help for the reference of all the commands.',
                    ]
                ),
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
        replyOrSend(emojies.robot + ' ' + errMsg, chatId, message)


def registerCommands():
    botApp.load_next_step_handlers()
