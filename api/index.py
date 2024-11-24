# -*- coding:utf-8 -*-


from core.appConfig import appConfig
from core.logger import getLogger
from core.flaskApp import flaskApp

from publicSite import publicSiteBlueprint, publicSiteDebugBlueprint
from bot.botBlueprint import botBlueprint

from bot.botApp import startBot

LOCAL = appConfig.get('LOCAL')

logger = getLogger('api/index')

# Missing variable `handler` or `app` in file "api/index.py".

app = flaskApp

__all__ = [
    # Export `app` variable
    'app',
]


startBot()


# XXX? Try to avoid twice starting bug...
#  run_main = os.environ.get('WERKZEUG_RUN_MAIN')
#  isMain = run_main == 'true'
doInit = True  # not LOCAL or isMain
# NOTE: Ensure initializing only once (avoiding double initialization with `* Restarting with stat`...)
if doInit:

    flaskApp.register_blueprint(publicSiteBlueprint, url_prefix='/')
    flaskApp.register_blueprint(publicSiteDebugBlueprint, url_prefix='/')

    flaskApp.register_blueprint(botBlueprint, url_prefix='/bot')


if __name__ == '__main__':
    token = appConfig.get('TELEGRAM_TOKEN')
    logger.debug('Token: %s' % token)
