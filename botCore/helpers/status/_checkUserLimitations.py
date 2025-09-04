from typing import Literal, cast

import telebot  # pyTelegramBotAPI
from dateutil.relativedelta import relativedelta
from prisma.models import MonthlyStats, TotalStats, UserStatus

from botCore.constants import emojies, limits
from botCore.helpers import replyOrSend
from botCore.types import TUserMode
from core.helpers.time import formatTime, getCurrentDateTime
from db.stats import getCurrentMonthStats, getTotalStats
from db.status import getUserStatus
from db.user import findUser

TUserAction = Literal['CAST', 'INFO']


def checkIfUserDeleted(message: telebot.types.Message, userId: int, showMessage: bool = True):
    user = findUser({'id': userId})

    if user and user.isDeleted:
        if showMessage:
            deletedAt = user.deletedAt or getCurrentDateTime()
            willBeDeletedAt = deletedAt + relativedelta(months=+1)
            content = f' Your account has been already marked to deletion on {formatTime("onlyDate", deletedAt)} (and will be wiped out on {formatTime("onlyDate", willBeDeletedAt)}). You can restore the account via /restore_account command.'
            replyOrSend(emojies.warning + ' ' + content, userId, message)
            return True

    return False


def checkUserLimitations(message: telebot.types.Message, userId: int, action: TUserAction):
    """
    Sends warnings and errors directly to the chat.
    Returns True if the action is allowed.
    """
    userStatus: UserStatus | None = getUserStatus(userId)
    userMode: TUserMode = cast(TUserMode, userStatus.userMode) if userStatus else 'GUEST'

    checkIfUserDeleted(message, userId, True)

    if userMode == 'PREMIUM':
        # No limitations
        return True

    if userMode == 'PAID':
        if not userStatus:
            content = 'There is something wrong with your account status data (no userStatus record found). Please contact administrator (@lilliputten) and ask to fix the issue.'
            replyOrSend(emojies.error + ' ' + content, userId, message)
            return False
        # paidAt = userStatus.paidAt
        # if not paidAt:
        #     content = 'There is something wrong with your account status data (no paidAt field found). Please contact administrator (@lilliputten) and ask to fix the issue.'
        #     replyOrSend(emojies.error + ' ' + content, userId, message)
        #     return False
        paymentValidUntil = userStatus.paymentValidUntil   # ensureCorrectDateTime(paidAt) + relativedelta(months=1)
        if not paymentValidUntil:
            content = 'There is something wrong with your account status data (no paymentValidUntil field found). Please contact administrator (@lilliputten) and ask to fix the issue.'
            replyOrSend(emojies.error + ' ' + content, userId, message)
            return False
        now = getCurrentDateTime()
        if now < paymentValidUntil:
            return True
        # Show a PAID plan expiration message and appy FREE plan
        content = '\n\n'.join(
            [
                f'YOUR PAID PERIOD ALREADY ENDED ON {formatTime("onlyDate", paymentValidUntil)}.',
                'The FREE usage plan is applied.',
                'Renew your subscription via /get_full_access or contact the administrator (@lilliputten).',
            ]
        )
        replyOrSend(emojies.warning + ' ' + content, userId, message)
        userMode = 'FREE'

    if userMode != 'GUEST' and userMode != 'FREE':
        content = f'Your are not allowed to make any requests. (Your plan is {userMode}.)'
        replyOrSend(emojies.error + ' ' + content, userId, message)
        return False

    # For FREE and GUEST modes calculate the valid limits...

    totalStats: TotalStats | None = getTotalStats(userId)
    currentStats: MonthlyStats | None = getCurrentMonthStats(userId)

    totalCastRequests = totalStats.requests if totalStats else 0
    totalInfoRequests = totalStats.infoRequests if totalStats else 0
    currentCastRequests = currentStats.requests if currentStats else 0
    currentInfoRequests = currentStats.infoRequests if currentStats else 0

    if userMode == 'GUEST':
        if action == 'CAST' and totalCastRequests >= limits.guestCastRequests:
            content = 'The limit of your guest download requests has been exceeded.'
            replyOrSend(emojies.error + ' ' + content, userId, message)
            return False
        if action == 'INFO' and totalInfoRequests >= limits.guestInfoRequests:
            content = 'The limit of your guest info requests has been exceeded.'
            replyOrSend(emojies.error + ' ' + content, userId, message)
            return False

    if userMode == 'FREE':
        if action == 'CAST' and currentCastRequests >= limits.freeCastRequests:
            content = 'The limit of your free download requests has been exceeded.'
            replyOrSend(emojies.error + ' ' + content, userId, message)
            return False
        if action == 'INFO' and currentInfoRequests >= limits.freeInfoRequests:
            content = 'The limit of your free info requests has been exceeded.'
            replyOrSend(emojies.error + ' ' + content, userId, message)
            return False

    return True  # OK, no limitations
