import traceback

from core.helpers import errorToString

from .._init import initDb
from ..models import TotalStats


def getTotalStats(userId: int):
    try:
        session = initDb()
        return session.get(TotalStats, userId)
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print('Error: ' + errMsg)
        return None
