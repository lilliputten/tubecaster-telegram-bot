import traceback

import telebot  # pyTelegramBotAPI
from prisma.models import UserStatus
from telebot import types

from botApp import botApp
from botCore.constants import emojies
from botCore.helpers import replyOrSend
from botCore.helpers.status import checkIfUserDeleted
from core.helpers.errors import errorToString
from core.helpers.time import formatTime, getCurrentDateTime
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, titleStyle, warningStyle
from db.status import getUserStatus

from .requestFullAccessPayment import requestFullAccessPayment
from .sendInfo import sendCommandInfo, sendQueryInfo

_logger = getDebugLogger()

_logTraceback = False


@botApp.message_handler(commands=['get_full_access'])
def requestFullAccess(message: types.Message):
    sendCommandInfo(message, 'requestFullAccess')
    userId = message.from_user.id if message.from_user else message.chat.id
    checkIfUserDeleted(message, userId, True)

    now = getCurrentDateTime()

    userStatus = getUserStatus(userId)

    # If there is an active paid subscription...
    if (
        userStatus
        and userStatus.userMode == 'PAID'
        and userStatus.paymentValidUntil
        and userStatus.paymentValidUntil > now
    ):
        showRequestFullAccessIfAlreadyPaidConfirmDialog(message, userStatus)
        return

    # # Option 1: Use intermediate confirmaiton dialog
    # showRequestFullAccessDialog(message)
    # Option 2: Immediately create an invoice
    requestFullAccessPayment(message, message.chat)


def showRequestFullAccessIfAlreadyPaidConfirmDialog(message: types.Message, userStatus: UserStatus):
    paymentValidUntil = userStatus.paymentValidUntil
    msgItems = [
        'YOU ALREADY HAVE A PAID USAGE PLAN.',
        f'Your current subscription is valid until {formatTime("onlyDate", paymentValidUntil)}.',
        'You can pay for the next paid period.',
        'In this case, the subscription period will be extended for another month, starting from the end of the current period.',
        'Do you want to pay now?',
    ]
    content = '\n\n'.join(filter(None, msgItems))
    markup = createRequestFullAccessButtonsMarkup()
    botApp.reply_to(
        message,
        emojies.question + ' ' + content,
        reply_markup=markup,
    )


# UNUSED: showRequestFullAccessDialog
# def showRequestFullAccessDialog(message: types.Message):
#     msgItems = [
#         'Are you sure you want to upgrade your account to a paid usage plan?',
#     ]
#     content = '\n\n'.join(filter(None, msgItems))
#     markup = createRequestFullAccessButtonsMarkup()
#     botApp.reply_to(
#         message,
#         emojies.question + ' ' + content,
#         reply_markup=markup,
#     )


def createRequestFullAccessButtonsMarkup():
    # @see https://core.telegram.org/bots/api#inlinekeyboardmarkup
    markup = types.InlineKeyboardMarkup(
        row_width=2,
    )
    # See https://core.telegram.org/bots/api#inlinekeyboardbutton
    yes = types.InlineKeyboardButton('Yes', callback_data='requestFullAccessYes')
    no = types.InlineKeyboardButton('No', callback_data='requestFullAccessNo')
    markup.add(yes, no)
    return markup


@botApp.callback_query_handler(lambda query: query.data == 'requestFullAccessYes')
def requestFullAccessYes(query: types.CallbackQuery):
    sendQueryInfo(query, 'requestFullAccessYes')
    message = query.message
    if not isinstance(message, types.Message):
        # NOTE: A normal message is required to register next step handler
        errMsg = 'Inaccessible message recieved!'
        _logger.error(errorStyle('requestFullAccessYes: Error: %s' % errMsg))
        botApp.send_message(message.chat.id, emojies.error + ' ' + errMsg)
        return
    userId = query.from_user.id if query.from_user else message.chat.id
    try:
        requestFullAccessPayment(message, message.chat)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error deleting user: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle(titleStyle('Traceback for the following error:') + sTraceback))
        _logger.error(errorStyle('requestFullAccessYes: ' + errMsg))
        replyOrSend(emojies.error + ' ' + errMsg, userId, message)


@botApp.callback_query_handler(lambda query: query.data == 'requestFullAccessNo')
def requestFullAccessNo(query: types.CallbackQuery):
    sendQueryInfo(query, 'requestFullAccessNo')
    message = query.message
    if isinstance(message, types.Message):
        botApp.delete_message(message.chat.id, message.id)
