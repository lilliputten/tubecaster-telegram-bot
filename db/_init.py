import traceback
from typing import Optional

from flask.ctx import _AppCtxGlobals

from core.helpers.errors import errorToString
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, primaryStyle, secondaryStyle, titleStyle, warningStyle
from prisma import Prisma, get_client, register

TGlobalCtx = _AppCtxGlobals

_db: Optional[Prisma] = None

_logger = getDebugLogger()

_logTraceback = False

# Already registered prisma creator
_hasBeenRegistered = False


def openDb(g: Optional[TGlobalCtx] = None) -> Prisma:
    global _db
    # gs = globals()
    if not _db:
        if g is not None and 'DB' in g:
            # Try to get db from global object...
            _db = g.DB
        _db = Prisma()
    if g is not None:
        # TODO: Check for _AppCtxGlobals
        g.DB = _db
    if not _db.is_connected():
        _db.connect()
    return _db


def closeDb(err: Optional[BaseException] = None):
    if err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'closeDb: Got error: ' + sError
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle('closeDb: Traceback for the following error:') + sTraceback)
        _logger.error(errorStyle(errMsg))

    try:
        client = get_client()
        if client.is_connected():
            client.disconnect()
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'closeDb: Caught error: ' + sError
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle('closeDb: Traceback for the following error:') + sTraceback)
        _logger.error(errorStyle(errMsg))


def initDb(g: Optional[TGlobalCtx] = None):
    global _hasBeenRegistered
    if not _hasBeenRegistered:
        register(openDb)
        _hasBeenRegistered = True
    # flaskApp.teardown_appcontext(closeDb)
    return openDb(g)
