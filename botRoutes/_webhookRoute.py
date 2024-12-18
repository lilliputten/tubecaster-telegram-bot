# -*- coding:utf-8 -*-

import traceback
from flask import Response
from flask import request
import telebot  # pyTelegramBotAPI

from core.appConfig import LOCAL
from core.helpers.errors import errorToString
from core.helpers.runtime import getModPath
from core.helpers.time import formatTime, getTimeStamp
from core.logger import getLogger
from core.utils import debugObj

from botApp import botApp

from botCore.botConfig import WEBHOOK_URL

from .botRoutes import botRoutes


startTimeStr = getTimeStamp()

_logger = getLogger(getModPath())

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
    messageId = message.id if message else None
    #  messageJson = message.json if message else None
    messageContentType = message.content_type if message else None
    messageChat = message.chat if message else None
    messageDate = formatTime(None, message.date) if message else None
    messageFromUser = message.from_user if message else None
    fromUserId = messageFromUser.id if messageFromUser else None
    fromUserUsername = messageFromUser.username if messageFromUser else None
    chatId = messageChat.id if messageChat else None
    obj = {
        'startTimeStr': startTimeStr,
        'timeStr': timeStr,
        'WEBHOOK_URL': WEBHOOK_URL,
        'LOCAL': LOCAL,
        'update': repr(update),
        'message': repr(message),
        #  'messageJson': repr(messageJson),
        'messageChat': repr(messageChat),
        'messageFromUser': repr(messageFromUser),
        'updateId': updateId,
        'messageText': messageText,
        'messageId': messageId,
        'messageContentType': messageContentType,
        'messageDate': messageDate,
        'fromUserId': fromUserId,
        'fromUserUsername': fromUserUsername,
        'chatId': chatId,
    }
    debugData = debugObj(obj)
    logContent = '\n'.join(
        [
            'webhookRoute: Update %d started' % updateId,
            debugData,
        ]
    )
    _logger.info(logContent)

    if update:
        try:
            if not update or not updateId:
                raise Exception('No update id provided!')
            botApp.process_new_updates([update])
            logContent = '\n'.join(
                [
                    'webhookRoute: Update %d finished' % updateId,
                    debugData,
                ]
            )
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

    return Response('OK', headers={'Content-type': 'text/plain'})
