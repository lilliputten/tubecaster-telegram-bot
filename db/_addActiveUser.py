import traceback
from prisma.models import User

from core.helpers.errors import errorToString


def addActiveUser(id: int, userStr: str):
    userClient = User.prisma()
    try:
        user = userClient.create(
            data={
                'id': id,
                'isActive': True,
                # 'userStr': userStr,
            },
        )
        return user
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print('Error: ' + errMsg)
        raise Exception(errMsg)
    finally:
        pass
