from ._init import initDb
from ._types import TCommandId
from .models import Command


def deleteCommandById(id: TCommandId):
    session = initDb()
    command = session.get(Command, id)
    if command is None:
        return None
    session.delete(command)
    session.commit()
    return command
