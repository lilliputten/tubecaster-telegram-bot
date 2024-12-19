from prisma import Prisma

from .types import TCommandId


def deleteCommandById(id: TCommandId):
    db = Prisma()
    try:
        if not db.is_connected():
            db.connect()
        # TODO: Check if this command (by messageId) exists in the database?
        return db.command.delete(
            where={
                'id': id,
            },
        )
    finally:
        db.disconnect()
