from prisma import Prisma

from .types import TNewCommandData


def addCommand(data: TNewCommandData):
    db = Prisma()
    try:
        if not db.is_connected():
            db.connect()
        # TODO: Check if this command (by messageId) exists in the database?
        command = db.command.create(
            data=data,
            # data={
            #     'updateId': updateId,
            #     'messageId': messageId,
            #     'userId': userId,
            #     'userStr': usernameStr,
            # },
        )
        return command
    finally:
        db.disconnect()
