from core.appConfig import appConfig
from core.logger import getLogger
from core.flaskApp import app

from publicSite.publicSiteBlueprint import publicSiteBlueprint
from bot.botBlueprint import botBlueprint


logger = getLogger('api/index')


logger.debug('Start')


# XXX? Try to avoid twice starting bug...
#  run_main = os.environ.get('WERKZEUG_RUN_MAIN')
#  isMain = run_main == 'true'
doInit = True  # not config['isDev'] or isMain

if doInit:  # NOTE: Ensure initializing only once (avoiding double initialization with `* Restarting with stat`...)

    app.register_blueprint(publicSiteBlueprint, url_prefix='/')
    app.register_blueprint(botBlueprint, url_prefix='/bot')


@app.route('/project-info')
def static_file():
    print('project-info')
    return app.send_static_file('project-info.txt')


if __name__ == '__main__':
    test = appConfig.get('TELEGRAM_TOKEN')
    #  logger.debug('main %s' % test)
