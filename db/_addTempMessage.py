from prisma.models import TempMessage

from ._types import TCommandId, TMessageId


def addTempMessage(
    commandId: TCommandId,
    messageId: TMessageId,
):
    try:
        # TODO: Check if this command (by messageId) exists in the database?
        tempMessageClient = TempMessage.prisma()
        tempMessage = tempMessageClient.create(
            data={
                'commandId': commandId,
                'messageId': messageId,
            },
        )
        return tempMessage
    finally:
        pass
