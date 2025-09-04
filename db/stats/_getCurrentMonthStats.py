from datetime import date

from ._getMonthlyStats import getMonthlyStats


def getCurrentMonthStats(userId: int):
    current_date = date.today()
    year = current_date.year
    month = current_date.month
    return getMonthlyStats(userId, year, month)
