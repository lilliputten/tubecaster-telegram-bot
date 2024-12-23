from prisma.models import TempMessage

from ._types import TCommandId


def getTempMessagesForCommand(
    commandId: TCommandId,
):
    try:
        # TODO: Check if this command (by messageId) exists in the database?
        tempMessageClient = TempMessage.prisma()
        tempMessages = tempMessageClient.find_many(
            where={
                'commandId': commandId,
            },
        )
        return tempMessages
    finally:
        pass
