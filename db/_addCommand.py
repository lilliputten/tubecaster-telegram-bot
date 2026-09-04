from ._init import initDb
from ._types import TNewCommandData
from .models import Command


def addCommand(data: TNewCommandData):
    session = initDb()
    command = Command(**data)
    session.add(command)
    session.commit()
    return command
