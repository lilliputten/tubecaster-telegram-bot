import traceback
from typing import Any, TypedDict, Union

from core.helpers.errors import errorToString

from .._init import initDb
from ..models import User

UserCommonData = dict[str, Any]


class UserUpdateData(TypedDict, total=False):
    userStr: str
    languageCode: str | None
    isDeleted: bool
    deletedAt: Any


def updateUser(
    userId: int,
    data: Union[UserCommonData, UserUpdateData],
):
    session = initDb()
    try:
        user = session.get(User, userId)
        payload = dict(data)
        if user is None:
            user = User(id=userId, **payload)
            session.add(user)
        else:
            for key, value in payload.items():
                setattr(user, key, value)
        session.commit()
        return user
    except Exception as err:
        session.rollback()
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print('Error: ' + errMsg)
        raise Exception(errMsg)
