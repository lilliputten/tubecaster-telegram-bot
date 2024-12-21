# -*- coding:utf-8 -*-

import traceback
from flask import Response

from core.appConfig import PROJECT_INFO
from core.helpers.errors import errorToString

from core.helpers.time import getTimeStamp
from core.logger import getDebugLogger, titleStyle, secondaryStyle
from core.utils import debugObj


from .botRoutes import botRoutes

startTimeStr = getTimeStamp()

_logger = getDebugLogger()

logTraceback = False


@botRoutes.route('/')
def rootRoute():
    """
    Root page:
    Start telegram bot with the current webhook (deployed to vercel or local exposed with ngrok)
    """
    timeStr = getTimeStamp()
    try:
        debugItems = {
            'timeStr': timeStr,
            'startTimeStr': startTimeStr,
        }
        debugStr = debugObj(debugItems)
        logItems = [
            'rootRoute: Empty test route',
            secondaryStyle(debugStr),
        ]
        logContent = '\n'.join(logItems)
        msgItems = [
            #  'Root route',
            'Application: %s' % PROJECT_INFO,
            #  debugStr,
        ]
        msgContent = '\n\n'.join(msgItems)
        _logger.info(logContent)
        return Response(msgContent, headers={'Content-type': 'text/plain'})
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'rootRoute: Error processing root route: ' + sError
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('rootRoute: Traceback for the following error:' + sTraceback)
        _logger.error(errMsg)
        return Response(errMsg, headers={'Content-type': 'text/plain'})
