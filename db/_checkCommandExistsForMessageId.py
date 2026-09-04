from sqlalchemy import select

from ._init import initDb
from ._types import TMessageId
from .models import Command


def checkCommandExistsForMessageId(messageId: TMessageId):
    session = initDb()
    command = session.scalars(select(Command).where(Command.messageId == messageId)).first()
    if command:
        command.repeated = (command.repeated or 0) + 1
        session.commit()
        return command
    return None
