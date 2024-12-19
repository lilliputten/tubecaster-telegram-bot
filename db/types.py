# from typing import (
#     TypedDict,
#     # Optional,
# )

from prisma.models import Command
from prisma.types import CommandCreateInput

TPrismaCommand = Command

TCommandId = int

TNewCommandData = CommandCreateInput

# class TNewCommandData(TypedDict):
#     updateId: int   # Type[Command.updateId]
#     messageId: int
#     userId: int
#     userStr: str


__all__ = [
    'TCommandId',
    'TPrismaCommand',
    'TNewCommandData',
]
