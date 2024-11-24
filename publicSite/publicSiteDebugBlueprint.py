# -*- coding:utf-8 -*-

from flask import Response
from flask import Blueprint
from datetime import datetime

import requests

from core.logger import getLogger

#  from core.logger import getDebugLog
from core.utils import stripHtml
from core.appConfig import appConfig


logger = getLogger('publicSite/publicSiteDebugBlueprint')

# @see https://flask.palletsprojects.com/en/stable/blueprints

publicSiteDebugBlueprint = Blueprint('publicSiteDebugBlueprint', __name__)

testNgrok = False

startTimeStr = datetime.today().strftime('%Y-%m-%d %H:%M:%S')


def showStartInfo():
    """
    Debug: Show application start info.
    """
    changed = appConfig.get('changed')
    LOCAL = appConfig.get('LOCAL')
    TELEGRAM_TOKEN = appConfig.get('TELEGRAM_TOKEN')
    WERKZEUG_RUN_MAIN = appConfig.get('WERKZEUG_RUN_MAIN')

    #  # Show environment (couldn't fit into vercel log records entirely)
    #  debugAppConfig = json.dumps(appConfig, indent=2)
    #  logger.info('appConfig: %s' % debugAppConfig)

    logger.info('Start: %s' % startTimeStr)
    logger.info('Changed: %s' % changed)
    logger.info('LOCAL: %s' % LOCAL)
    logger.info('TELEGRAM_TOKEN: %s' % TELEGRAM_TOKEN)
    logger.info('WERKZEUG_RUN_MAIN: %s' % WERKZEUG_RUN_MAIN)
    #  print('Start print: %s: %s' % (changed, TELEGRAM_TOKEN))


def debugVar(obj, key: str):
    """
    Debug helper: create object variable line, if exists.
    """
    val = obj.get(key)
    if not val:
        return None
    return key + ': ' + str(val)


@publicSiteDebugBlueprint.route('/test')
def debug():
    timeStr = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    testStr = 'TEST ' + timeStr
    # Show log entry...
    logger.info('LOG ' + testStr)
    obj = {
        **{
            'startTimeStr': startTimeStr,
            'timeStr': timeStr,
        },
        **appConfig,
    }
    # Send sample log data manually...
    if testNgrok:
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
        obj['url'] = url
        obj['resText'] = stripHtml(response.text)
    #  # DEBUG: Get logging debug info
    #  # Make a pause before checking debug log
    #  time.sleep(1)
    #  obj['debugLog'] = getDebugLog()
    # Debug data object
    text = '\n'.join(
        list(
            filter(
                None,
                map(
                    lambda a: debugVar(obj, a),
                    [
                        'startTimeStr',
                        'timeStr',
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
    res = Response(text)
    res.headers['Content-type'] = 'text/plain'
    return res


showStartInfo()
