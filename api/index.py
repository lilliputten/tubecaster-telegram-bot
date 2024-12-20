# -*- coding:utf-8 -*-

from core.appConfig import LOCAL, PROJECT_INFO, WERKZEUG_RUN_MAIN, isNormalRun

from core.logger import getDebugLogger
from core.helpers.time import formatTime
from core.utils import debugObj


_logger = getDebugLogger()


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
    from botRoutes import botRoutes

    from botCommands import registerCommands

    flaskApp.register_blueprint(botRoutes, url_prefix='/')

    # Start commands
    registerCommands()


# Expose `app` variable
app = flaskApp
__all__ = ['app']


if __name__ == '__main__':
    _logger.debug('PROJECT_INFO: %s' % PROJECT_INFO)
