import traceback

from ._updateUser import updateUser


def ensureValidUser(userId: int, userStr: str, languageCode: str | None):
    return updateUser(
        userId,
        {
            'userStr': userStr,
            'languageCode': languageCode,
        },
    )
