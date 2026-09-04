from sqlalchemy import select

from ._init import initDb
from ._types import TCommandId
from .models import TempMessage


def getTempMessagesForCommand(
    commandId: TCommandId,
):
    session = initDb()
    return list(session.scalars(select(TempMessage).where(TempMessage.commandId == commandId)).all())
