# -*- coding:utf-8 -*-

import sysconfig
import traceback

from core.appConfig import LOCAL, PROJECT_INFO, WERKZEUG_RUN_MAIN, appConfig, isNormalRun
from core.helpers.errors import errorToString
from core.helpers.time import formatTime
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, primaryStyle, secondaryStyle, warningStyle
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
        # NOTE: It's possible to encounter a bug if `EXT_SUFFIX` values will be different in different enviroments
        'EXT_SUFFIX': sysconfig.get_config_var('EXT_SUFFIX'),
        # NOTE: Used manual setting for prisma query engine path variable (`PRISMA_QUERY_ENGINE_BINARY`) in `/var/www/.uwsgi-apps/flask-tubecaster.ini`
        'PRISMA_QUERY_ENGINE_BINARY': appConfig.get('PRISMA_QUERY_ENGINE_BINARY'),
        # NOTE: Timezone (set in `/var/www/.uwsgi-apps/flask-tubecaster.ini`)
        'TZ': appConfig.get('TZ'),
    }
    logItems = [
        primaryStyle('Application started'),
        secondaryStyle(debugObj(debugItems)),
    ]
    logContent = '\n'.join(logItems)
    _logger.info(logContent)


showDebug()


from flaskApp import flaskApp

if isNormalRun:
    try:
        from botCommands import registerCommands
        from botRoutes import botRoutes

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
            _logger.warning(warningStyle('Traceback for the following error:') + sTraceback)
        _logger.error(errorStyle(errMsg))
        raise err


# Expose `app` variable
app = flaskApp
__all__ = ['app']


if __name__ == '__main__':
    _logger.info('PROJECT_INFO: %s' % PROJECT_INFO)
