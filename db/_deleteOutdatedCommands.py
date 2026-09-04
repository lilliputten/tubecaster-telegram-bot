import datetime
import traceback
from datetime import date

from sqlalchemy import delete

from core.helpers.errors import errorToString

from ._init import initDb
from .models import Command

validHours = 1


def deleteOutdatedCommands(outdatedDate: date | datetime.datetime | None = None):
    session = initDb()
    try:
        now = datetime.datetime.now(datetime.timezone.utc)
        if outdatedDate is None:
            outdatedDate = now - datetime.timedelta(hours=validHours)
        result = session.execute(delete(Command).where(Command.createdAt < outdatedDate))
        session.commit()
        return result.rowcount
    except Exception as err:
        session.rollback()
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print('Error: ' + errMsg)
        raise Exception(errMsg)
