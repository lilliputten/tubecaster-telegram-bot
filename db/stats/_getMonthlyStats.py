import traceback

from core.helpers import errorToString

from .._init import initDb
from ..models import MonthlyStats


def getMonthlyStats(userId: int, year: int, month: int):
    try:
        session = initDb()
        return session.get(MonthlyStats, (userId, year, month))
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print('Error: ' + errMsg)
        return None
