# -*- coding:utf-8 -*-

from core.appConfig import appConfig, LOCAL, PROJECT_INFO
from core.helpers.time import formatTime
from core.logger import getLogger
from flaskApp.flaskApp import flaskApp
from botRoutes.botRoutes import botRoutes

from botCommands import registerCommands

WERKZEUG_RUN_MAIN = appConfig.get('WERKZEUG_RUN_MAIN')

logger = getLogger('api/index')

timeStr = formatTime()

logger.info(
    'App started, PROJECT_INFO=%s, LOCAL=%s, WERKZEUG_RUN_MAIN=%s, time=%s'
    % (PROJECT_INFO, LOCAL, WERKZEUG_RUN_MAIN, timeStr)
)

flaskApp.register_blueprint(botRoutes, url_prefix='/')

# Start commands
registerCommands()


# Expose `app` variable
app = flaskApp
__all__ = ['app']


if __name__ == '__main__':
    token = appConfig.get('TELEGRAM_TOKEN')
    logger.debug('Token: %s' % token)
