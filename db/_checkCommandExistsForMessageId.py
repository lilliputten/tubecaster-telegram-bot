from prisma.models import Command

from ._types import TMessageId


def checkCommandExistsForMessageId(messageId: TMessageId):
    commandClient = Command.prisma()
    try:
        command = commandClient.find_first(
            where={
                'messageId': messageId,
            },
        )
        if command:
            # Update counter and return the object if exists...
            commandClient.update(
                where={'id': command.id},
                data={'repeated': {'increment': 1}},
            )
            return command
        # Return falsy value otherwise (all is ok)
        return None
    finally:
        pass
