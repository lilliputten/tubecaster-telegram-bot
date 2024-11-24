#  import json
#  import flask
#  from flask import make_response
from datetime import datetime
import logging

from core.appConfig import appConfig
from core.logger import getLogger, getDebugLog
from core.flaskApp import app

from core.utils.stripHtml import stripHtml

#  from publicSite.publicSiteBlueprint import publicSiteBlueprint
#  from bot.botBlueprint import botBlueprint

import requests

#  from requests.adapters import HTTPAdapter

#  from bot.botApp import botApp

#  changed = """
#  @changed 2024.11.24, 01:18
#  """.strip().replace(
#      '@changed ', ''
#  )


logger = getLogger('api/index')


changed = appConfig.get('changed')
LOCAL = appConfig.get('LOCAL')
TELEGRAM_TOKEN = appConfig.get('TELEGRAM_TOKEN')
WERKZEUG_RUN_MAIN = appConfig.get('WERKZEUG_RUN_MAIN')

#  debugAppConfig = json.dumps(appConfig, indent=2)
#  logger.info('appConfig: %s' % debugAppConfig)

#  logging.getLogger().handlers.clear()

timeStr = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
logger.info('INFO: %s' % timeStr)
logger.info('Start: %s' % timeStr)
logger.info('Changed: %s' % changed)
logger.info('LOCAL: %s' % LOCAL)
logger.info('TELEGRAM_TOKEN: %s' % TELEGRAM_TOKEN)
logger.info('WERKZEUG_RUN_MAIN: %s' % WERKZEUG_RUN_MAIN)
#  print('Start print: %s: %s' % (changed, TELEGRAM_TOKEN))


#  botApp.run_polling()


# XXX? Try to avoid twice starting bug...
#  run_main = os.environ.get('WERKZEUG_RUN_MAIN')
#  isMain = run_main == 'true'
doInit = True  # not config['isDev'] or isMain

#  if doInit:  # NOTE: Ensure initializing only once (avoiding double initialization with `* Restarting with stat`...)
#
#      app.register_blueprint(publicSiteBlueprint, url_prefix='/')
#      app.register_blueprint(botBlueprint, url_prefix='/bot')


@app.route('/project-info')
def static_file():
    print('project-info')
    return app.send_static_file('project-info.txt')


# DEBUG!
def debugVar(obj, key: str):
    val = obj.get(key)
    if not val:
        return None
    return key + ': ' + str(val)


@app.route('/')
def debug():
    timeStr = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    testStr = 'TEST ' + timeStr
    # Show log entry...
    logger.info('LOG ' + testStr)
    # Send sample log data manually...
    url = 'https://93a7-178-140-11-63.ngrok-free.app:443'
    sendData = {
        'message': 'MANUAL ' + testStr,
        'asctime': 'asctime',
        'pathname': 'pathname',
        'lineno': 'lineno',
        'name': 'name',
        'levelname': 'levelname',
    }
    response = requests.post(url, json=sendData)
    resText = stripHtml(response.text)
    # Get logging debug info
    debugLog = getDebugLog()
    # Debug data object
    obj = {
        **{
            'url': url,
            'resText': resText,
            'debugLog': debugLog,
        },
        **appConfig,
    }
    text = '\n'.join(
        list(
            filter(
                None,
                map(
                    lambda a: debugVar(obj, a),
                    [
                        'changed',
                        'LOCAL',
                        'resText',
                        'url',
                        'debugLog',
                        # ...
                        'TELEGRAM_TOKEN',
                        'WERKZEUG_RUN_MAIN',
                        'USE_LOGS_SERVER',
                        'USE_SYSLOG_SERVER',
                        'LOGS_FILE',
                        'SYSLOG_HOST',
                        'SYSLOG_PORT',
                        'LOGS_SERVER_PREFIX',
                        'LOGS_SERVER_HOST',
                        'LOGS_SERVER_PORT',
                        'LOGS_SERVER_RETRIES',
                    ],
                ),
            )
        )
    )
    #  resp = flask.Response(text)
    #  resp.headers['Content-type'] = 'text/plain'
    #  response = make_response(text, 200)
    #  response.mimetype = "text/plain"
    return '<pre>' + text + '</pre>'
    #  return text


if __name__ == '__main__':
    test = appConfig.get('TELEGRAM_TOKEN')
    #  logger.debug('main %s' % test)
