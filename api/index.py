# -*- coding:utf-8 -*-


from core.appConfig import appConfig
from core.logger import getLogger
from core.flaskApp import flaskApp

from publicSite import publicSiteBlueprint, publicSiteDebugBlueprint
from bot.botBlueprint import botBlueprint

#  from bot.botApp import botApp


logger = getLogger('api/index')


#  botApp.run_polling()


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
