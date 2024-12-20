from prisma import Prisma

from .types import TCommandId, TMessageId


def addTempMessage(
    commandId: TCommandId,
    messageId: TMessageId,
):
    db = Prisma()
    try:
        if not db.is_connected():
            db.connect()
        # TODO: Check if this command (by messageId) exists in the database?
        tempMessage = db.tempmessage.create(
            data={
                'commandId': commandId,
                'messageId': messageId,
            },
        )
        return tempMessage
    finally:
        db.disconnect()
