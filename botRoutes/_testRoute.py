# -*- coding:utf-8 -*-

import time
import traceback
from flask import Response
from flask import request

from core.appConfig import LOCAL, appConfig, PROJECT_INFO
from core.helpers.errors import errorToString

from core.helpers.strings import truncStr
from core.helpers.time import getTimeStamp
from core.logger import getDebugLogger, loggerConfig
from core.utils import debugObj
from core.utils.generic import dictFromModule

from botApp import botApp
from botCore import botConfig
from botCore.botConfig import WEBHOOK_URL

from .botRoutes import botRoutes


startTimeStr = getTimeStamp()

_logger = getDebugLogger()

logTraceback = False


@botRoutes.route('/test')
def testRoute():
    """
    Get the deep debugging info
    """
    try:
        timeStr = getTimeStamp()
        titleStr = 'testRoute: Test @ %s' % timeStr
        debugItems = {
            'timeStr': timeStr,
            'startTimeStr': startTimeStr,
            #  'headers': debugObj(dict(request.headers)),
            #  'environ': debugObj(dict(request.environ)),
            'PROJECT_INFO': PROJECT_INFO,
            #  'requestDict': debugObj(request.__dict__),
            'LOGS_SERVER_HOST': appConfig.get('LOGS_SERVER_HOST'),
            'LOGS_SERVER_URL': loggerConfig.LOGS_SERVER_URL,
            'LOGS_SERVER_PORT': appConfig.get('LOGS_SERVER_PORT'),
            'YT_COOKIE': truncStr(appConfig.get('YT_COOKIE', 'NONE'), 50),
            'WEBHOOK_URL': WEBHOOK_URL,
            'LOCAL': LOCAL,
        }
        debugStr = debugObj(debugItems)
        logItems = [
            titleStr,
            debugStr,
        ]
        logContent = '\n'.join(logItems)
        msgItems = [
            titleStr,
            debugStr,
        ]
        msgContent = '\n\n'.join(msgItems)
        _logger.info(logContent)
        #  raise Exception('Debugging error') # DEBUG
        return Response(msgContent, headers={'Content-type': 'text/plain'})
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'testRoute: Error processing test route: ' + sError
        if logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('testRoute: Traceback for the following error:' + sTraceback)
        _logger.error(errMsg)
        return Response(errMsg, headers={'Content-type': 'text/plain'})
