from prisma.models import Command

from .types import TNewCommandData


def addCommand(data: TNewCommandData):
    commandClient = Command.prisma()
    try:
        command = commandClient.create(
            data=data,
        )
        return command
    finally:
        pass
