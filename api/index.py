# -*- coding:utf-8 -*-

import traceback
from core.appConfig import LOCAL, PROJECT_INFO, WERKZEUG_RUN_MAIN, isNormalRun

from core.helpers.errors import errorToString
from core.logger import getDebugLogger
from core.helpers.time import formatTime
from core.utils import debugObj


_logger = getDebugLogger()

_logTraceback = False


def showDebug():
    """
    Debug: Show application start info.
    """
    timeStr = formatTime()
    debugItems = {
        'PROJECT_INFO': PROJECT_INFO,
        'LOCAL': LOCAL,
        'WERKZEUG_RUN_MAIN': WERKZEUG_RUN_MAIN,
        'isNormalRun': isNormalRun,
        'timeStr': timeStr,
    }
    logItems = [
        'Application started',
        debugObj(debugItems),
    ]
    logContent = '\n'.join(logItems)
    _logger.info(logContent)


showDebug()


from flaskApp import flaskApp

if isNormalRun:
    try:
        from botRoutes import botRoutes
        from botCommands import registerCommands

        # Register routes
        flaskApp.register_blueprint(botRoutes, url_prefix='/')

        # Start commands
        registerCommands()
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'Error caught: ' + sError
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('Traceback for the following error:' + sTraceback)
        _logger.error(errMsg)
        raise err


from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


def testPydantic():
    try:

        class User(BaseModel):
            id: int
            name: str = 'John Doe'
            signup_ts: Optional[datetime] = None
            friends: List[int] = []

        external_data = {
            'id': '123',
            'signup_ts': '2017-06-01 12:22',
            'friends': [1, '2', b'3'],
        }

        user = User(**external_data)

        print(user)
        # > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]

        print(user.id)
        # > 123
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'testPydantic: Error caught: ' + sError
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('TtestPydantic: raceback for the following error:' + sTraceback)
        _logger.error(errMsg)


testPydantic()


# Expose `app` variable
app = flaskApp
__all__ = ['app']


if __name__ == '__main__':
    _logger.debug('PROJECT_INFO: %s' % PROJECT_INFO)
