from typing import TypedDict

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .._init import initDb
from ..models import User


class UserWhereInput(TypedDict, total=False):
    id: int
    isDeleted: bool


class UserInclude(TypedDict, total=False):
    userStatus: bool
    totalStats: bool
    monthlyStats: bool


default_include: UserInclude = {
    'userStatus': True,
    'totalStats': True,
    'monthlyStats': True,
}


def findUser(where: UserWhereInput, include: UserInclude = default_include):
    session = initDb()
    stmt = select(User)
    if include.get('userStatus'):
        stmt = stmt.options(selectinload(User.userStatus))
    if include.get('totalStats'):
        stmt = stmt.options(selectinload(User.totalStats))
    if include.get('monthlyStats'):
        stmt = stmt.options(selectinload(User.monthlyStats))
    if 'id' in where:
        stmt = stmt.where(User.id == where['id'])
    if 'isDeleted' in where:
        stmt = stmt.where(User.isDeleted == where['isDeleted'])
    return session.scalars(stmt).first()
