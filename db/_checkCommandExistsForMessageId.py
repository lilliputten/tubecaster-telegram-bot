from prisma import Prisma

from .types import TMessageId


def checkCommandExistsForMessageId(messageId: TMessageId):
    db = Prisma()
    try:
        if not db.is_connected():
            db.connect()
        command = db.command.find_first(
            where={
                'messageId': messageId,
            },
        )
        if command:
            # Update counter and return the object if exists...
            db.command.update(
                where={'id': command.id},
                data={'repeated': {'increment': 1}},
            )
            return command
        # Return falsy value otherwise (all is ok)
        return None
    finally:
        db.disconnect()
