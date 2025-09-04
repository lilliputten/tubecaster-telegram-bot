import traceback
from datetime import datetime

from dateutil.relativedelta import relativedelta
from prisma.models import User

from core.helpers import errorToString


def wipeOutDeletedUsers():
    """
    Remove all user records marked for deletion earlier than a month ago
    """
    deletedAt = datetime.now() - relativedelta(months=1)
    userClient = User.prisma()
    try:
        user = userClient.delete_many(
            where={
                'deletedAt': {
                    'lt': deletedAt,
                },
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
