# -*- coding:utf-8 -*-

import traceback
from datetime import datetime
from random import randrange

import telebot  # pyTelegramBotAPI
from dateutil.relativedelta import relativedelta
from telebot import types

from botApp import botApp
from botCore.constants import emojies, limits
from botCore.helpers import getUserName
from botCore.helpers._replyOrSend import replyOrSend
from core.appConfig import (
    CONTROLLER_CHANNEL_ID,
    LOCAL,
    LOGGING_CHANNEL_ID,
    PROJECT_INFO,
    PROJECT_PATH,
    TELEGRAM_OWNER_ID,
)
from core.constants import defaultLanguageCode
from core.helpers.errors import errorToString
from core.helpers.strings import removeAnsiStyles
from core.helpers.time import formatTime, getCurrentDateTime
from core.logger import errorStyle, getDebugLogger, secondaryStyle, titleStyle, warningStyle
from core.utils import debugObj
from db.status import getUserStatus, updateUserStatus
from db.user import ensureValidUser

_logger = getDebugLogger()

_logTraceback = False


def requestFullAccessPayment(message: types.Message, user: types.User | types.Chat):
    chatId = message.chat.id
    userId = user.id
    userName = getUserName(user)
    json = message.json
    json = json.get('reply_to_message', json)
    fromData: dict = json.get('from', {})
    languageCode = str(fromData.get('language_code', defaultLanguageCode))
    try:
        # DEBUG
        debugItems = {
            'timeStr': formatTime(),
            'userId': userId,
            'chatId': chatId,
            'userName': userName,
            'LOCAL': LOCAL,
        }
        logItems = [
            titleStyle('requestFullAccessPayment'),
            secondaryStyle(debugObj(debugItems)),
        ]
        logContent = '\n'.join(logItems)
        _logger.info(logContent)

        isEmulation = LOCAL or userId == TELEGRAM_OWNER_ID
        amount = 1 if isEmulation else limits.paidPlanPriceStars

        paymentName = 'TubeCasterBot Full Access'

        prices = [
            types.LabeledPrice(
                label=paymentName,
                # Price in XTR stars
                amount=amount,
            ),
        ]

        descrItems = [
            'Get unlimited access to all TubeCaster bot features for a month.',
            'The PAID usage plan includes an unlimited number of requests to download YouTube audio and receive video details.',
            "See usage plans' details for more information via the /plans command.",
        ]

        payload = ':'.join([str(userId), userName.replace(':', '-'), languageCode])
        invoiceMessage = botApp.send_invoice(
            chatId,
            title=paymentName,
            description=' '.join(descrItems),
            invoice_payload=payload,
            provider_token=None,  # '284685063:TEST:YjQ2Y2EzMWFlMw' if LOCAL else None,  # Leave empty for Stars
            currency=limits.currency,
            prices=prices,
        )

        # DEBUG: Mock the successfull payment handler invocation
        if isEmulation and LOCAL:
            # payment: types.SuccessfulPayment = {}
            payment = types.SuccessfulPayment(
                currency=limits.currency,  # Currency code, e.g., 'XTR'
                total_amount=amount,  # Amount in smallest units (cents)
                invoice_payload=payload,  # The invoice payload string you passed before
                telegram_payment_charge_id='abc' + str(randrange(100, 999)),  # Telegram payment charge id (mock)
                provider_payment_charge_id='def' + str(randrange(100, 999)),  # Provider payment charge id (mock)
            )
            invoiceMessage.successful_payment = payment
            handlePayment(invoiceMessage)

        # # NOTE: Don't show a message: there will the telegram invoice appear instead
        # contentItems = [
        #     'Your payment invoice already created.',
        #     'You will receive it in the chat and then you can pay it.',
        # ]
        # replyOrSend(emojies.success + ' ' + '\n\n'.join(contentItems), userId, message)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error processing default command: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle(titleStyle('Traceback for the following error:') + sTraceback))
        _logger.error(errorStyle('requestFullAccessPayment: ' + errMsg))
        replyOrSend(emojies.robot + ' ' + errMsg, userId, message)


# Handler for pre-checkout query: approve payment
@botApp.pre_checkout_query_handler(func=lambda _: True)
def handlePreCheckout(pre_checkout_query):
    try:
        # Log the pre-checkout query
        _logger.info(f'Pre-checkout query received: {pre_checkout_query.id}')
        # Approve payment (must be fast - within 10 seconds)
        botApp.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
        _logger.info(f'Pre-checkout query approved: {pre_checkout_query.id}')
    except Exception as err:
        _logger.error(f'Error in pre-checkout handler: {err}')
        # Still try to approve even if there's an error
        try:
            botApp.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
        except:
            pass


# Handler for successful payment messages
@botApp.message_handler(content_types=['successful_payment'])
def handlePayment(message: types.Message):
    payment = message.successful_payment
    userId = message.from_user.id if message.from_user else message.chat.id

    try:
        if not payment:
            raise Exception('Received empty payment info.')

        chargeId = payment.provider_payment_charge_id
        tgChargeId = payment.telegram_payment_charge_id
        amount = payment.total_amount
        currency = payment.currency
        payload = payment.invoice_payload
        [userIdStr, userName, languageCode] = payload.split(':')
        userId = int(userIdStr)
        if not userId:
            raise Exception('Undefined user id.')

        now = getCurrentDateTime()
        paymentValidUntil = now + relativedelta(months=1)

        # Ensure if the user is already created
        user = ensureValidUser(userId, userName, languageCode)

        # Check currernt paid status. If there is active paid subscription, than extend the subscription period
        userStatus = getUserStatus(userId)
        if (
            userStatus
            and userStatus.userMode == 'PAID'
            and userStatus.paymentValidUntil
            and userStatus.paymentValidUntil > now
        ):
            paymentValidUntil = userStatus.paymentValidUntil + relativedelta(months=1)

        userStatus = updateUserStatus(
            userId,
            {
                'userMode': 'PAID',
                'statusChangedAt': now,
                'paidAt': now,
                'paymentValidUntil': paymentValidUntil,
                'paymentId': chargeId,
            },
        )

        contentItems = [
            'YOUR PAYMENT ALREADY RECEIVED!',
            f'You are now on a PAID plan util {formatTime("onlyDate", paymentValidUntil)}.',
            'Use the /status command to show the current account status.',
        ]
        replyOrSend(emojies.success + ' ' + '\n\n'.join(contentItems), userId, message)

        # DEBUG
        debugItems = {
            'timeStr': formatTime(None, now),
            'paymentValidUntil': formatTime(None, paymentValidUntil),
            'userId': userId,
            'userName': userName,
            'languageCode': languageCode,
            # 'usernameStr': getUserName(message.from_user),
            'LOCAL': LOCAL,
            'chargeId': chargeId,
            'tgChargeId': tgChargeId,
            'amount': amount,
            'currency': currency,
        }
        logItems = [
            titleStyle('handlePayment:')
            + f' The user {userName} with id {userId} has paid {amount} {currency} for the PAID plan invoice {chargeId}.',
            secondaryStyle(debugObj(debugItems)),
        ]
        logContent = '\n'.join(logItems)
        _logger.info(logContent)

        # Send info to the controller
        botApp.send_message(CONTROLLER_CHANNEL_ID, emojies.money + ' ' + removeAnsiStyles(logContent))

    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error processing default command: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle(titleStyle('Traceback for the following error:') + sTraceback))
        _logger.error(errorStyle('handlePayment: ' + errMsg))
        replyOrSend(emojies.robot + ' ' + errMsg, userId, message)
