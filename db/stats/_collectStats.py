from .._init import initDb


def collectStats(userId: int):
    prisma = initDb()

    # Get TotalStats
    totalStats = prisma.totalstats.find_unique(
        where={
            'userId': userId,
        },
    )

    # Get MonthlyStats sorted by year desc, month desc
    monthlyStats = prisma.monthlystats.find_many(
        where={
            'userId': userId,
        },
        order=[
            {'year': 'desc'},
            {'month': 'desc'},
        ],
    )

    return (totalStats, monthlyStats)
    # return {
    #     'total': totalStats,
    #     'monthly': monthlyStats,
    # }
