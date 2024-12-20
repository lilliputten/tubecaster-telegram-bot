# -*- coding:utf-8 -*-

import traceback
from typing import Optional
from flask import Response
from flask import request
import telebot  # pyTelegramBotAPI

from core.appConfig import LOCAL
from core.helpers.errors import errorToString
from core.helpers.time import formatTime, getTimeStamp
from core.logger import getDebugLogger
from core.utils import debugObj

# \<\(dbTypes\|checkCommandExistsForMessageId\|addCommand\|deleteCommandById\|addTempMessage\)\>
# from db import types as dbTypes, checkCommandExistsForMessageId, addCommand, deleteCommandById, addTempMessage

from botApp import botApp

from botCore.constants import emojies
from botCore.helpers import getUserName
from botCore.botConfig import WEBHOOK_URL

from .botRoutes import botRoutes


startTimeStr = getTimeStamp()

_logger = getDebugLogger()

logTraceback = False


@botRoutes.route('/webhook', methods=['POST'])
def webhookRoute():
    """
    Process the telegram bot webhook.
    """
    timeStr = getTimeStamp()
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
    message = update.message if update else None
    messageText = message.text if message else None
    messageId = message.id if message else 0
    #  messageJson = message.json if message else None
    messageContentType = message.content_type if message else None
    messageChat = message.chat if message else None
    messageDate = formatTime(None, message.date) if message else None
    user = message.from_user if message else None
    userId = user.id if user else 0
    usernameStr = getUserName(user)
    chatId = messageChat.id if messageChat else None
    debugData = {
        'startTimeStr': startTimeStr,
        'timeStr': timeStr,
        'WEBHOOK_URL': WEBHOOK_URL,
        'LOCAL': LOCAL,
        'update': repr(update),
        'message': repr(message),
        #  'messageJson': repr(messageJson),
        'messageChat': repr(messageChat),
        'user': repr(user),
        'updateId': updateId,
        'messageText': messageText,
        'messageId': messageId,
        'messageContentType': messageContentType,
        'messageDate': messageDate,
        'userId': userId,
        'usernameStr': usernameStr,
        'chatId': chatId,
    }
    debugStr = debugObj(debugData)
    logItems = [
        'webhookRoute: Update %d for message %d started' % (updateId, messageId),
        debugStr,
    ]
    logContent = '\n'.join(logItems)
    _logger.info(logContent)

    if update:
        # createdCommand: Optional[dbTypes.TPrismaCommand] = None
        try:
            if not update or not updateId:
                raise Exception('No update id has been provided!')
            if not messageId:
                raise Exception('No message id has been provided!')

            existedCommand = False   # checkCommandExistsForMessageId(messageId)
            if existedCommand:
                # Command already exists, do nothing, but notify user
                debugData = {
                    'commandId': existedCommand.id,
                    'repeated': existedCommand.repeated,
                    'createdAtStr': formatTime(None, existedCommand.createdAt),
                    'updatedAtStr': formatTime(None, existedCommand.updatedAt),
                    'timeStr': timeStr,
                    'messageChat': repr(messageChat),
                    'updateId': updateId,
                    'messageText': messageText,
                    'messageId': messageId,
                    'messageContentType': messageContentType,
                    'messageDate': messageDate,
                    'userId': userId,
                    'usernameStr': usernameStr,
                    'chatId': chatId,
                }
                debugStr = debugObj(debugData)
                logItems = [
                    'webhookRoute: Update %d for message %d is already processing' % (updateId, messageId),
                    debugStr,
                ]
                logContent = '\n'.join(logItems)
                _logger.info(logContent)
                # TODO: Update message: Find first temp message and
                if chatId:
                    newMessage = botApp.send_message(
                        chatId,
                        emojies.waiting + ' Your command is still processing, be patient, please...',
                    )
                    # addTempMessage(commandId=existedCommand.id, messageId=newMessage.id)
            else:
                # # Create new command
                # commandData: dbTypes.TNewCommandData = {
                #     'updateId': updateId,
                #     'messageId': messageId,
                #     'userId': userId,
                #     'userStr': usernameStr,
                # }
                # createdCommand = addCommand(commandData)

                # Process the command...
                botApp.process_new_updates([update])

                debugData = {
                    # 'commandId': createdCommand.id,
                    # 'createdAtStr': formatTime(None, createdCommand.createdAt),
                    # 'updatedAtStr': formatTime(None, createdCommand.updatedAt),
                    'timeStr': timeStr,
                    'messageChat': repr(messageChat),
                    'updateId': updateId,
                    'messageText': messageText,
                    'messageId': messageId,
                    'messageContentType': messageContentType,
                    'messageDate': messageDate,
                    'userId': userId,
                    'usernameStr': usernameStr,
                    'chatId': chatId,
                }
                debugStr = debugObj(debugData)
                logItems = [
                    'webhookRoute: Update %d for message %d is already processing' % (updateId, messageId),
                    debugStr,
                ]
                logContent = '\n'.join(logItems)

                _logger.info(logContent)
        except Exception as err:
            sError = errorToString(err, show_stacktrace=False)
            sTraceback = str(traceback.format_exc())
            errMsg = 'webhookRoute: Error processing webhook update: ' + sError
            if logTraceback:
                errMsg += sTraceback
            else:
                _logger.info('webhookRoute: Traceback for the following error:' + sTraceback)
            _logger.error(errMsg)
            return Response(errMsg, headers={'Content-type': 'text/plain'})
        finally:
            pass
            # # Remove created command...
            # if createdCommand:
            #     # TODO: Remove temp messages
            #     deleteCommandById(createdCommand.id)

    return Response('OK', headers={'Content-type': 'text/plain'})
