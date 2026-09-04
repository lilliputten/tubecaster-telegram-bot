import traceback
from typing import Optional

from flask.ctx import _AppCtxGlobals
from sqlalchemy.orm import Session

from core.helpers.errors import errorToString
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, warningStyle

from .database import close_sessions, get_session_factory

TGlobalCtx = _AppCtxGlobals

_logger = getDebugLogger()

_logTraceback = False


def openDb(g: Optional[TGlobalCtx] = None) -> Session:
    # Cache the Engine and scoped_session factory (process-wide). A single
    # Session instance is not shared across requests; scoped_session keeps a
    # thread-local session, which is the usual SQLAlchemy practice.
    if g is not None and 'DB' in g and g.DB is not None:
        return g.DB

    session_factory = get_session_factory()
    session = session_factory()

    if g is not None:
        g.DB = session

    return session


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
        close_sessions()
    except Exception as closeErr:
        sError = errorToString(closeErr, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'closeDb: Caught error: ' + sError
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle('closeDb: Traceback for the following error:') + sTraceback)
        _logger.error(errorStyle(errMsg))


def initDb(g: Optional[TGlobalCtx] = None) -> Session:
    return openDb(g)


__all__ = [
    'closeDb',
    'initDb',
    'openDb',
]
