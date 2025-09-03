# from typing import Optional
from prisma.models import User
from prisma.types import types

default_include: types.UserInclude = {
    'userStatus': True,
    'totalStats': True,
    'monthlyStats': True,
}


def findUser(where: types.UserWhereInput, include: types.UserInclude = default_include):
    userClient = User.prisma()
    try:
        user = userClient.find_first(
            where=where,
            include=include,
        )
        return user
    finally:
        pass
