# -*- coding:utf-8 -*-

from core.appConfig import appConfig, LOCAL, PROJECT_INFO

from core.logger import getDebugLogger
from core.helpers.time import formatTime


from core.utils import debugObj
from flaskApp import flaskApp
from botRoutes import botRoutes

from botCommands import registerCommands


_logger = getDebugLogger()


def showDebug():
    """
    Debug: Show application start info.
    """
    timeStr = formatTime()
    debugItems = {
        'PROJECT_INFO': PROJECT_INFO,
        'LOCAL': LOCAL,
        'WERKZEUG_RUN_MAIN': appConfig.get('WERKZEUG_RUN_MAIN'),
        'timeStr': timeStr,
    }
    logItems = [
        'Application started',
        debugObj(debugItems),
    ]
    logContent = '\n'.join(logItems)
    _logger.info(logContent)


# Start the actual app
def startApp():
    showDebug()

    flaskApp.register_blueprint(botRoutes, url_prefix='/')

    # Start commands
    registerCommands()

    return flaskApp


# Expose `app` variable
app = startApp()
__all__ = ['app']


if __name__ == '__main__':
    _logger.debug('PROJECT_INFO: %s' % PROJECT_INFO)
