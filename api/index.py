# -*- coding:utf-8 -*-


from core.appConfig import appConfig, LOCAL, PROJECT_INFO, TELEGRAM_TOKEN
from core.logger import getLogger
from flaskApp.flaskApp import flaskApp

from bot.botRoutes import botRoutes

WERKZEUG_RUN_MAIN = appConfig.get('WERKZEUG_RUN_MAIN')

logger = getLogger('api/index')

logger.info('App started, PROJECT_INFO=%s, LOCAL=%s, WERKZEUG_RUN_MAIN=%s' % (PROJECT_INFO, LOCAL, WERKZEUG_RUN_MAIN))

flaskApp.register_blueprint(botRoutes, url_prefix='/')

# Expose `app` variable
app = flaskApp
__all__ = ['app']


if __name__ == '__main__':
    token = TELEGRAM_TOKEN
    logger.debug('Token: %s' % token)
