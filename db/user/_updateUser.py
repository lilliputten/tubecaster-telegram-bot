import traceback
from typing import Union, cast

from prisma.models import User
from prisma.types import UserCreateInput, UserUpdateInput

from core.helpers.errors import errorToString

# Use Union to accept fields from either type
UserCommonData = Union[UserCreateInput, UserUpdateInput]


def updateUser(
    userId: int,
    data: UserCommonData,
):
    userClient = User.prisma()
    try:
        createData = cast(UserCreateInput, {'id': userId, **data})
        updateData = cast(UserUpdateInput, data)

        user = userClient.upsert(
            where={'id': userId},
            data={
                'create': createData,
                'update': updateData,
            },
        )
        return user
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print('Error: ' + errMsg)
        raise Exception(errMsg)
