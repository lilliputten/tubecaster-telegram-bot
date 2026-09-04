from datetime import date

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from .._init import initDb
from ..models import MonthlyStats, TotalStats


def updateStats(userId: int, requests: int = 0, infoRequests: int = 0, failures: int = 0, volume: int = 0):
    current_date = date.today()
    year = current_date.year
    month = current_date.month

    session = initDb()
    try:
        total_stmt = insert(TotalStats).values(
            userId=userId,
            requests=requests,
            infoRequests=infoRequests,
            failures=failures,
            volume=volume,
        )
        total_stmt = total_stmt.on_conflict_do_update(
            index_elements=[TotalStats.userId],
            set_={
                'requests': TotalStats.requests + requests,
                'infoRequests': TotalStats.infoRequests + infoRequests,
                'failures': TotalStats.failures + failures,
                'volume': TotalStats.volume + volume,
            },
        )
        session.execute(total_stmt)

        monthly_stmt = insert(MonthlyStats).values(
            userId=userId,
            year=year,
            month=month,
            requests=requests,
            infoRequests=infoRequests,
            failures=failures,
            volume=volume,
        )
        monthly_stmt = monthly_stmt.on_conflict_do_update(
            index_elements=[MonthlyStats.userId, MonthlyStats.year, MonthlyStats.month],
            set_={
                'requests': MonthlyStats.requests + requests,
                'infoRequests': MonthlyStats.infoRequests + infoRequests,
                'failures': MonthlyStats.failures + failures,
                'volume': MonthlyStats.volume + volume,
            },
        )
        session.execute(monthly_stmt)
        session.commit()
    except Exception:
        session.rollback()
        raise
