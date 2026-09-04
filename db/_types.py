from datetime import datetime
from typing import TypedDict

from .models import Command, TempMessage

TCommand = Command
TPrismaCommand = Command

TCommandId = int
TMessageId = int

TTempMessage = TempMessage


class TNewCommandData(TypedDict, total=False):
    updateId: int
    messageId: int
    userId: int
    userStr: str
    repeated: int
    isActive: bool
    createdAt: datetime
    updatedAt: datetime


__all__ = [
    'TCommandId',
    'TMessageId',
    'TCommand',
    'TPrismaCommand',
    'TNewCommandData',
    'TTempMessage',
]
