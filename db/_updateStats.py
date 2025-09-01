from datetime import date

# from prisma import Prisma

from ._init import initDb


# New signature:
# def updateStats(userId: int, volume: int):
def updateStats(userId: int, requests: int = 0, infoRequests: int = 0, failures: int = 0, volume: int = 0):
    current_date = date.today()
    year = current_date.year
    month = current_date.month

    prisma = initDb()

    with prisma.tx() as tx:
        # Update or create TotalStats
        tx.totalstats.upsert(
            where={
                'userId': userId,
            },
            data={
                'create': {
                    'userId': userId,
                    'requests': requests,
                    'infoRequests': infoRequests,
                    'failures': failures,
                    'volume': volume,
                },
                'update': {
                    'requests': {
                        'increment': requests,
                    },
                    'infoRequests': {
                        'increment': infoRequests,
                    },
                    'failures': {
                        'increment': failures,
                    },
                    'volume': {
                        'increment': volume,
                    },
                },
            },
        )
        # Update or create MonthlyStats
        tx.monthlystats.upsert(
            where={
                'userId_year_month': {
                    'userId': userId,
                    'year': year,
                    'month': month,
                },
            },
            data={
                'create': {
                    'userId': userId,
                    'year': year,
                    'month': month,
                    'requests': requests,
                    'infoRequests': infoRequests,
                    'failures': failures,
                    'volume': volume,
                },
                'update': {
                    'requests': {
                        'increment': requests,
                    },
                    'infoRequests': {
                        'increment': infoRequests,
                    },
                    'failures': {
                        'increment': failures,
                    },
                    'volume': {
                        'increment': volume,
                    },
                },
            },
        )
