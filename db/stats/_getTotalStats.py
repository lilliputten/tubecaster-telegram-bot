import traceback

from prisma.models import TotalStats

from core.helpers import errorToString


def getTotalStats(userId: int):
    try:
        totalStatsClient = TotalStats.prisma()
        totalStats = totalStatsClient.find_unique(
            where={
                'userId': userId,
            },
        )
        return totalStats
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print('Error: ' + errMsg)
        return None
