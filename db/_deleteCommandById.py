from prisma.models import Command

from ._types import TCommandId


def deleteCommandById(id: TCommandId):
    commandClient = Command.prisma()
    try:
        return commandClient.delete(
            where={
                'id': id,
            },
        )
    finally:
        pass
