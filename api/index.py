# -*- coding:utf-8 -*-


from core.appConfig import appConfig
from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger
from flaskApp.flaskApp import flaskApp

#  from publicSite import publicSiteBlueprint, publicSiteDebugBlueprint
from bot.botRoutes import botRoutes

from bot.botApp import botApp

LOCAL = appConfig.get('LOCAL')
WERKZEUG_RUN_MAIN = appConfig.get('WERKZEUG_RUN_MAIN')

logger = getLogger('api/index')

logger.info('App started, LOCAL=%s, WERKZEUG_RUN_MAIN=%s' % (LOCAL, WERKZEUG_RUN_MAIN))

# Missing variable `handler` or `app` in file "api/index.py".

# XXX? Try to avoid twice starting bug...
isMain = WERKZEUG_RUN_MAIN == 'true'
doInit = True  # not LOCAL or isMain
# NOTE: Ensure initializing only once (avoiding double initialization with `* Restarting with stat`...)
if doInit:

    #  flaskApp.register_blueprint(publicSiteBlueprint, url_prefix='/')
    #  flaskApp.register_blueprint(publicSiteDebugBlueprint, url_prefix='/')

    flaskApp.register_blueprint(botRoutes, url_prefix='/')

# Expose `app` variable
app = flaskApp
__all__ = ['app']


#  startBot()


if __name__ == '__main__':
    token = appConfig.get('TELEGRAM_TOKEN')
    logger.debug('Token: %s' % token)
