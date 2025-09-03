# -*- coding:utf-8 -*-

import traceback
from typing import Optional

import telebot  # pyTelegramBotAPI
from flask import Response, request

from botApp import botApp
from botCore.constants import emojies
from botCore.helpers import getUserName
from core.appConfig import LOCAL
from core.helpers.errors import errorToString
from core.helpers.time import formatTime
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, primaryStyle, secondaryStyle, titleStyle, warningStyle
from db import (
    addCommand,
    addTempMessage,
    checkCommandExistsForMessageId,
    deleteCommandById,
    deleteOutdatedCommands,
    deleteOutdatedTempMessages,
    getTempMessagesForCommand,
)
from db import types as dbTypes
from db import wipeOutDeletedUsers

from .botRoutes import botRoutes

startTimeStr = formatTime()

_logger = getDebugLogger()

logTraceback = False


@botRoutes.route('/webhook', methods=['POST'])
def webhookRoute():
    """
    Core access point: Process the telegram bot webhook.
    """
    requestStream = request.stream.read().decode('utf-8')
    update = telebot.types.Update.de_json(requestStream)
    #  Sample update data: <telebot.types.Update object at 0x0000024A1904B5C0>
    #  chosen_inline_result = None
    #  deleted_business_messages = None
    #  edited_business_message = None
    #  edited_channel_post = None
    #  edited_message = None
    #  inline_query = None
    #  message = <telebot.types.Message object at 0x0000024A1904B560>
    #  message_reaction = None
    #  message_reaction_count = None
    #  my_chat_member = None
    #  poll = None
    #  poll_answer = None
    #  pre_checkout_query = None
    #  purchased_paid_media = None
    #  removed_chat_boost = None
    #  shipping_query = None
    #  update_id = 574259009
    updateId = update.update_id if update else None
    callback_query = update.callback_query if update else None
    message = update.message if update else None
    if not message and callback_query:
        message = callback_query.message
    messageText = message.text if message else None
    messageId = message.id if message else 0
    messageChat = message.chat if message else None
    user = message.from_user if message else None
    userId = user.id if user else 0
    usernameStr = getUserName(user)
    chatId = messageChat.id if messageChat else None
    # # DEBUG
    # # messageContentType = message.content_type if message else None
    # # messageDate = formatTime(None, message.date) if message else None
    # timeStr = formatTime()
    # stateValue = botApp.get_state(userId, chatId)
    # debugData = {
    #     'startTimeStr': startTimeStr,
    #     'timeStr': timeStr,
    #     # 'WEBHOOK_URL': WEBHOOK_URL,
    #     'LOCAL': LOCAL,
    #     'update': repr(update),
    #     'message': repr(message),
    #     'callback_query': repr(callback_query),
    #     'messageChat': repr(messageChat),
    #     'user': repr(user),
    #     'updateId': updateId,
    #     'messageText': messageText,
    #     'messageId': messageId,
    #     # 'messageContentType': messageContentType,
    #     # 'messageDate': messageDate,
    #     'userId': userId,
    #     'usernameStr': usernameStr,
    #     'chatId': chatId,
    #     'stateValue': stateValue,
    # }
    # debugStr = debugObj(debugData)
    # logItems = [
    #     titleStyle('webhookRoute: Update %d for message %d started' % (updateId, messageId)),
    #     secondaryStyle(debugStr),
    # ]
    # logContent = '\n'.join(logItems)
    # _logger.info(logContent)

    # Remove previous message markup
    if callback_query and callback_query.message:
        botApp.edit_message_reply_markup(chat_id=chatId, message_id=callback_query.message.id, reply_markup=None)

    # Check for active user (add this check into the restricted commands)...
    # newMessage = botApp.send_message(
    #     chatId,
    #     'Test Message',
    # )
    # return Response('Test', headers={'Content-type': 'text/plain'})

    createdCommand: Optional[dbTypes.TPrismaCommand] = None
    try:
        if not update or not updateId:
            raise Exception('No update id has been provided!')
        if not messageId:
            raise Exception('No message id has been provided!')

        existedCommand = checkCommandExistsForMessageId(messageId) if messageId else None
        if existedCommand:
            # Command already exists, do nothing, but notify user
            # # DEBUG
            # debugData = {
            #     'commandId': existedCommand.id,
            #     'repeated': existedCommand.repeated,
            #     'createdAtStr': formatTime(None, existedCommand.createdAt),
            #     'updatedAtStr': formatTime(None, existedCommand.updatedAt),
            #     'timeStr': timeStr,
            #     'messageChat': repr(messageChat),
            #     'updateId': updateId,
            #     'messageText': messageText,
            #     'messageId': messageId,
            #     'messageContentType': messageContentType,
            #     'messageDate': messageDate,
            #     'userId': userId,
            #     'usernameStr': usernameStr,
            #     'chatId': chatId,
            # }
            # debugStr = debugObj(debugData)
            # logItems = [
            #     titleStyle('webhookRoute: Update %d for message %d is already processing' % (updateId, messageId)),
            #     secondaryStyle(debugStr),
            # ]
            # logContent = '\n'.join(logItems)
            # _logger.info(logContent)
            if chatId:
                # fmt: off
                infoStr = ' '.join(filter(None, [
                    emojies.sleeping,
                    'Your command',
                    '(%s)' % messageText if messageText else None,
                    'is still being processed, be patient, please...',
                ]))
                # fmt: on
                newMessage = botApp.send_message(
                    chatId,
                    infoStr,
                    disable_web_page_preview=True,
                )
                addTempMessage(commandId=existedCommand.id, messageId=newMessage.id)
        else:
            # Create new command
            commandData: dbTypes.TNewCommandData = {
                'updateId': updateId,
                'messageId': messageId,
                'userId': userId,
                'userStr': usernameStr,
            }
            createdCommand = addCommand(commandData)

            # Process the command...
            botApp.process_new_updates([update])

            # DEBUG: Local test: try adding (and removing later, see `finally` section) a temp message...
            if LOCAL and chatId and messageText == 'test':
                newMessage = botApp.send_message(
                    chatId,
                    emojies.warning + ' Test temp message',
                )
                addTempMessage(commandId=createdCommand.id, messageId=newMessage.id)

            # # DEBUG
            # stateValue = botApp.get_state(userId, chatId)
            # debugData = {
            #     'commandId': createdCommand.id,
            #     'createdAtStr': formatTime(None, createdCommand.createdAt),
            #     'updatedAtStr': formatTime(None, createdCommand.updatedAt),
            #     'timeStr': timeStr,
            #     'messageChat': repr(messageChat),
            #     'updateId': updateId,
            #     'messageText': messageText,
            #     'messageId': messageId,
            #     'messageContentType': messageContentType,
            #     'messageDate': messageDate,
            #     'userId': userId,
            #     'usernameStr': usernameStr,
            #     'chatId': chatId,
            #     'stateValue': stateValue,
            # }
            # debugStr = debugObj(debugData)
            # logItems = [
            #     titleStyle('webhookRoute: Update %d for message %d has been processed' % (updateId, messageId)),
            #     secondaryStyle(debugStr),
            # ]
            # logContent = '\n'.join(logItems)
            # _logger.info(logContent)
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'webhookRoute: Error processing webhook update: ' + sError
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle('webhookRoute: Traceback for the following error:') + sTraceback)
        _logger.error(errorStyle(errMsg))
        return Response(errMsg, headers={'Content-type': 'text/plain'})
    finally:
        # TODO: To reset the current action?
        # if chatId:
        #     botApp.send_chat_action(chatId, action=None)
        # Remove created command...
        if createdCommand:
            # Remove temp messages...
            if chatId:
                tempMessages = getTempMessagesForCommand(createdCommand.id)
                if len(tempMessages):
                    tempMessageIds = list(
                        map(
                            lambda it: it.messageId,
                            tempMessages,
                        )
                    )
                    botApp.delete_messages(chat_id=chatId, message_ids=tempMessageIds)
            # Delete all command data...
            deleteCommandById(createdCommand.id)
            # Delete all outdated commands & messages...
            deleteOutdatedCommands()
            deleteOutdatedTempMessages()
            # Check and clean well outdated deleted accounts (removed alder than mpnth ago)
            wipeOutDeletedUsers()
        # # DEBUG
        # stateValue = botApp.get_state(userId, chatId)
        # debugStr = debugObj({**debugData, 'stateValue': stateValue })
        # logItems = [
        #     titleStyle('webhookRoute: Update %d for message %d finished' % (updateId, messageId)),
        #     secondaryStyle(debugStr),
        # ]
        # logContent = '\n'.join(logItems)
        # _logger.info(logContent)

    return Response('OK', headers={'Content-type': 'text/plain'})
