from ._init import initDb
from ._types import TCommandId, TMessageId
from .models import TempMessage


def addTempMessage(
    commandId: TCommandId,
    messageId: TMessageId,
):
    session = initDb()
    tempMessage = TempMessage(
        commandId=commandId,
        messageId=messageId,
    )
    session.add(tempMessage)
    session.commit()
    return tempMessage
