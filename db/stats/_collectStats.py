from sqlalchemy import select

from .._init import initDb
from ..models import MonthlyStats, TotalStats


def collectStats(userId: int):
    session = initDb()

    totalStats = session.get(TotalStats, userId)

    monthlyStats = list(
        session.scalars(
            select(MonthlyStats)
            .where(MonthlyStats.userId == userId)
            .order_by(MonthlyStats.year.desc(), MonthlyStats.month.desc())
        ).all()
    )

    return (totalStats, monthlyStats)
