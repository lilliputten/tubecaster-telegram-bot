import traceback
from prisma.models import UserStatus

from core.helpers import errorToString


def getUserStatus(userId: int):
    try:
        userStatusClient = UserStatus.prisma()
        userStatus = userStatusClient.find_unique(
            where={
                'userId': userId,
            },
        )
        return userStatus
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print('Error: ' + errMsg)
        return None
