from datetime import date

# from prisma import Prisma

from ._init import initDb


def updateStats(userId: int, volume: int):
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
                    'requests': 1,
                    'volume': volume,
                },
                'update': {
                    'requests': {
                        'increment': 1,
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
                    'requests': 1,
                    'volume': volume,
                },
                'update': {
                    'requests': {
                        'increment': 1,
                    },
                    'volume': {
                        'increment': volume,
                    },
                },
            },
        )
