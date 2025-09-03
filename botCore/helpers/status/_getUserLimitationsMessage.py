from prisma.models import MonthlyStats, TotalStats, UserStatus
from typing import Literal
from botCore.constants import limits
from botCore.types import TUserMode

from db.status import getUserStatus
from db.stats import getCurrentMonthStats, getTotalStats
from typing import cast


TUserAction = Literal['CAST', 'INFO']


def getUserLimitationsMessage(userId: int, action: TUserAction):
    """
    Returns an error message error if user exceed some limits.
    Returns an empty value (None) on success.
    """
    userStatus: UserStatus | None = getUserStatus(userId)
    userMode: TUserMode = cast(TUserMode, userStatus.userMode) if userStatus else 'GUEST'

    totalStats: TotalStats | None = getTotalStats(userId)
    currentStats: MonthlyStats | None = getCurrentMonthStats(userId)

    totalCastRequests = totalStats.requests if totalStats else 0
    totalInfoRequests = totalStats.infoRequests if totalStats else 0
    currentCastRequests = currentStats.requests if currentStats else 0
    currentInfoRequests = currentStats.infoRequests if currentStats else 0

    if userMode == 'GUEST':
        if action == 'CAST' and totalCastRequests >= limits.guestCastRequests:
            return 'The limit of your guest download requests has been exceeded.'
        if action == 'INFO' and totalInfoRequests >= limits.guestInfoRequests:
            return 'The limit of your guest info requests has been exceeded.'
    elif userMode == 'FREE':
        if action == 'CAST' and currentCastRequests >= limits.freeCastRequests:
            return 'The limit of your free download requests has been exceeded.'
        if action == 'INFO' and currentInfoRequests >= limits.freeInfoRequests:
            return 'The limit of your free info requests has been exceeded.'
    elif userMode != 'PAID':
        return 'Your are not allowed to make any requests.'

    return None  # OK, no limitations
