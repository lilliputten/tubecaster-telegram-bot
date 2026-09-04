import traceback
from typing import Any, TypedDict, Union

from core.helpers.errors import errorToString

from .._init import initDb
from ..models import UserStatus

UserStatusCommonData = dict[str, Any]


class UserStatusUpdateData(TypedDict, total=False):
    userMode: str
    statusChangedAt: Any
    paidAt: Any
    paymentValidUntil: Any
    paymentId: str | None


def updateUserStatus(
    userId: int,
    data: Union[UserStatusCommonData, UserStatusUpdateData],
):
    session = initDb()
    try:
        userStatus = session.get(UserStatus, userId)
        payload = dict(data)
        if userStatus is None:
            userStatus = UserStatus(userId=userId, **payload)
            session.add(userStatus)
        else:
            for key, value in payload.items():
                setattr(userStatus, key, value)
        session.commit()
        return userStatus
    except Exception as err:
        session.rollback()
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print('Error: ' + errMsg)
        raise Exception(errMsg)
