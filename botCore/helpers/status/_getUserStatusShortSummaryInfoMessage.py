from datetime import datetime
from typing import cast

from dateutil.relativedelta import relativedelta
from prisma.models import MonthlyStats, TotalStats, UserStatus

from botCore.constants import limits
from botCore.types import TUserMode
from core.helpers.time import ensureCorrectDateTime, formatTime, getCurrentDateTime
from db.stats import getCurrentMonthStats, getTotalStats
from db.status import getUserStatus
from db.user import findUser


def getUserStatusShortSummaryInfoMessage(userId: int):
    """
    Returns an error message error if user exceed some limits.
    Returns an empty value (None) on success.
    """
    user = findUser({'id': userId})

    userStatus: UserStatus | None = getUserStatus(userId)
    userMode: TUserMode = cast(TUserMode, userStatus.userMode) if userStatus else 'GUEST'

    totalStats: TotalStats | None = getTotalStats(userId)
    currentStats: MonthlyStats | None = getCurrentMonthStats(userId)

    totalCastRequests = totalStats.requests if totalStats else 0
    totalInfoRequests = totalStats.infoRequests if totalStats else 0
    currentCastRequests = currentStats.requests if currentStats else 0
    currentInfoRequests = currentStats.infoRequests if currentStats else 0

    limitsItems = []

    if userMode == 'PAID':
        if userStatus:
            paidAt = userStatus.paidAt
            if paidAt:
                validUntil = ensureCorrectDateTime(paidAt) + relativedelta(months=+1)
                now = getCurrentDateTime()
                if now < validUntil:
                    limitsItems.append(
                        '\n\n'.join(
                            [
                                f"You're on a {userMode} usage plan.",
                                f'Your paid subscription is valid until {formatTime("onlyDate", validUntil)}.',
                                'You have unlimited requests amount.',
                            ]
                        )
                    )
                else:
                    limitsItems.append(
                        '\n\n'.join(
                            [
                                f'You had a PAID usage plan, but your subscription has already ended on {formatTime("onlyDate", validUntil)}.',
                                # 'Instead, a FREE data plan is used.',
                            ]
                        )
                    )
                    userMode = 'FREE'

    isGuest = userMode == 'GUEST'
    isFree = userMode == 'FREE'

    if isGuest or isFree:
        castRequestsLimit = limits.guestCastRequests if isGuest else limits.freeCastRequests
        infoRequestsLimit = limits.guestInfoRequests if isGuest else limits.freeInfoRequests
        castRequestsCount = totalCastRequests if isGuest else currentCastRequests
        infoRequestsCount = totalInfoRequests if isGuest else currentInfoRequests
        castRequestsAvailable = max(0, castRequestsLimit - castRequestsCount)
        infoRequestsAvailable = max(0, infoRequestsLimit - infoRequestsCount)
        limitsItems.append(f"You're on a {userMode} usage plan.")
        limitsItems.append('You have:')
        limitsItems.append(
            '\n'.join(
                [
                    f'- {castRequestsAvailable} of {castRequestsLimit} download requests;',
                    f'- {infoRequestsAvailable} of {infoRequestsLimit} info requests.',
                ]
            )
        )
        limitsItems.append(
            'You can upgrade your plan if you need more via '
            + ('/become_user or /get_full_access commands.' if isGuest else '/get_full_access command.')
        )
        limitsItems.append('See available /plans info.')
    elif userMode != 'PAID':
        limitsItems.append("You're in the restricted mode.")
        limitsItems.append('See /plans info for options to upgrade your account.')

    if user and user.isDeleted:
        deletedAt = user.deletedAt or getCurrentDateTime()
        willBeDeletedAt = deletedAt + relativedelta(months=1)
        limitsItems.append(
            f'Your account has been marked to deletion on {formatTime("onlyDate", deletedAt)} (and will be wiped out on {formatTime("onlyDate", willBeDeletedAt)}). You can restore the account via /restore_account command.'
        )

    limitsItems.append('Ask any questions to the administrator (@lilliputten).')

    content = '\n\n'.join(list(filter(None, limitsItems)))

    return content
