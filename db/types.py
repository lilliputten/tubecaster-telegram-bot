# from typing import (
#     TypedDict,
#     # Optional,
# )

from prisma.models import Command, TempMessage
from prisma.types import CommandCreateInput

TPrismaCommand = Command

TCommandId = int
TMessageId = int

TNewCommandData = CommandCreateInput

TTempMessage = TempMessage

# class TNewCommandData(TypedDict):
#     updateId: int   # Type[Command.updateId]
#     messageId: int
#     userId: int
#     userStr: str


__all__ = [
    'TCommandId',
    'TMessageId',
    'TPrismaCommand',
    'TNewCommandData',
    'TTempMessage',
]
