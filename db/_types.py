from prisma.models import Command, TempMessage
from prisma.types import CommandCreateInput

TPrismaCommand = Command

TCommandId = int
TMessageId = int

TNewCommandData = CommandCreateInput

TTempMessage = TempMessage


__all__ = [
    'TCommandId',
    'TMessageId',
    'TPrismaCommand',
    'TNewCommandData',
    'TTempMessage',
]
