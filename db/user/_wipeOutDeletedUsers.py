import traceback
from datetime import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import delete

from core.helpers import errorToString

from .._init import initDb
from ..models import User


def wipeOutDeletedUsers():
    """
    Remove all user records marked for deletion earlier than a month ago
    """
    deletedAt = datetime.now() - relativedelta(months=1)
    session = initDb()
    try:
        result = session.execute(delete(User).where(User.deletedAt < deletedAt))
        session.commit()
        return result.rowcount  # type: ignore
    except Exception as err:
        session.rollback()
        errText = errorToString(err, show_stacktrace=False)
        sTraceback = '\n\n' + str(traceback.format_exc()) + '\n\n'
        errMsg = 'Error: ' + errText
        print('Traceback for the following error:' + sTraceback)
        print('Error: ' + errMsg)
        raise Exception(errMsg)
