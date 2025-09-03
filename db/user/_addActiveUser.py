import traceback
from datetime import datetime

from core.helpers import errorToString
from core.logger import errorStyle, getDebugLogger, secondaryStyle, titleStyle, warningStyle
from db import initDb

_logger = getDebugLogger()

_logTraceback = False


def addActiveUser(userId: int, userStr: str, languageCode: str | None):
    prisma = initDb()
    try:
        user = prisma.user.upsert(
            where={'id': userId},
            data={
                'create': {
                    'id': userId,
                    'userStr': userStr,
                    'languageCode': languageCode,
                },
                'update': {
                    'userStr': userStr,
                    'languageCode': languageCode,
                    'isDeleted': False,  # Clear deleted flag, just for case
                    'createdAt': datetime.now(),  # Update created timestamp forcibly
                },
            },
        )
        return user
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error ensuring user: ' + errText
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle(titleStyle('Traceback for the following error:') + sTraceback))
        _logger.error(errorStyle('addActiveUser: ' + errMsg))
        raise Exception(errMsg)
