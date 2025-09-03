from datetime import datetime
from dateutil.relativedelta import relativedelta

from prisma.models import MonthlyStats, TotalStats, UserStatus
from botCore.constants import limits
from botCore.types import TUserMode

from core.helpers.time import formatTime
from db.user import findUser
from db.status import getUserStatus
from db.stats import getCurrentMonthStats, getTotalStats
from typing import cast


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

    isGuest = userMode == 'GUEST'
    isFree = userMode == 'FREE'
    isPaid = userMode == 'PAID'
    # isDenied = userMode == 'DENIED'

    limitsItems = []
    if isGuest or isFree:
        limitsItems.append(f"You're on the {userMode} usage plan.")
        castRequestsLimit = limits.guestCastRequests if isGuest else limits.freeCastRequests
        infoRequestsLimit = limits.guestInfoRequests if isGuest else limits.freeInfoRequests
        castRequestsCount = totalCastRequests if isGuest else currentCastRequests
        infoRequestsCount = totalInfoRequests if isGuest else currentInfoRequests
        castRequestsAvailable = max(0, castRequestsLimit - castRequestsCount)
        infoRequestsAvailable = max(0, infoRequestsLimit - infoRequestsCount)
        limitsItems.append(f'You have: {castRequestsAvailable} (of {castRequestsLimit}) download')
        limitsItems.append(f'and {infoRequestsAvailable} (of {infoRequestsLimit}) info')
        limitsItems.append('requests available.')
        limitsItems.append('You can upgrade your plan if you need more')
        if isGuest:
            limitsItems.append('via /become_user or /get_full_access commands.')
        else:
            limitsItems.append('via /get_full_access command.')
        limitsItems.append('See available /plans info.')
    elif isPaid:
        pass
        # limitsItems.append("You have unlimited download and info requests amount.")
    else:
        limitsItems.append("You're in the restricted mode.")
        limitsItems.append('See /plans info to upgrade your account or ask an administrator at @lilliputten.')

    if user and user.isDeleted:
        deletedAt = user.deletedAt or datetime.now()
        willBeDeletedAt = deletedAt + relativedelta(months=+1)
        limitsItems.append(
            f'Your account has been marked to deletion on {formatTime("onlyDate", deletedAt)} (and will be wiped out on {formatTime("onlyDate", willBeDeletedAt)}). You can restore the account via /restore_account command.'
        )

    content = ' '.join(list(filter(None, limitsItems)))

    return content
