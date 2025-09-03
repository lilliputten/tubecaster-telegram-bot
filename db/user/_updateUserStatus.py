import traceback
from prisma.models import UserStatus

from botCore.types._TUserMode import TUserMode
from core.helpers.errors import errorToString


def updateUserStatus(userId: int, userMode: TUserMode):
    userStatusClient = UserStatus.prisma()
    try:
        userStatus = userStatusClient.upsert(
            where={
                'userId': userId,
            },
            data={
                'create': {
                    'userId': userId,
                    'userMode': userMode,
                },
                'update': {
                    'userMode': userMode,
                },
            },
        )
        return userStatus
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print('Error: ' + errMsg)
        raise Exception(errMsg)
    finally:
        pass
