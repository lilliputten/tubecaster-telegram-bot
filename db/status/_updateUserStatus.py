import traceback
from typing import Union, cast

from prisma.models import UserStatus
from prisma.types import UserStatusCreateInput, UserStatusUpdateInput

from core.helpers.errors import errorToString

# Use Union to accept fields from either type
UserStatusCommonData = Union[UserStatusCreateInput, UserStatusUpdateInput]


def updateUserStatus(
    userId: int,
    data: UserStatusCommonData,
):
    userStatusClient = UserStatus.prisma()
    try:
        createData = cast(UserStatusCreateInput, {'userId': userId, **data})
        updateData = cast(UserStatusUpdateInput, data)

        userStatus = userStatusClient.upsert(
            where={'userId': userId},
            data={
                'create': createData,
                'update': updateData,
            },
        )
        return userStatus
    except Exception as err:
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print('Error: ' + errMsg)
        raise Exception(errMsg)
