from datetime import date
import traceback
from prisma.models import MonthlyStats

from core.helpers import errorToString


def getMonthlyStats(userId: int, year: int, month: int):
    try:
        monthlyStatsClient = MonthlyStats.prisma()
        monthlyStats = monthlyStatsClient.find_unique(
            where={
                'userId_year_month': {
                    'userId': userId,
                    'year': year,
                    'month': month,
                }
            },
        )
        return monthlyStats
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print('Error: ' + errMsg)
        return None
