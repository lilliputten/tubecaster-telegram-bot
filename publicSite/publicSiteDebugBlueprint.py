# -*- coding:utf-8 -*-

from flask import Response
from flask import Blueprint
from datetime import datetime

import requests

from core.helpers.timeStamp import getTimeStamp
from core.logger import getLogger

#  from core.logger import getDebugLog
from core.utils import debugObj, stripHtml, variableAndKeyString
from core.appConfig import appConfig


logger = getLogger('publicSite/publicSiteDebugBlueprint')

# @see https://flask.palletsprojects.com/en/stable/blueprints

publicSiteDebugBlueprint = Blueprint('publicSiteDebugBlueprint', __name__)

testNgrok = False

startTimeStr = getTimeStamp(True)


@publicSiteDebugBlueprint.route('/test')
def debug():
    timeStr = getTimeStamp(True)
    testStr = 'TEST ' + timeStr
    logger.info('LOG ' + testStr)

    TELEGRAM_TOKEN = appConfig.get('TELEGRAM_TOKEN')
    changed = appConfig.get('changed')

    logger.info('Started: %s' % startTimeStr)
    logger.info('Changed: %s' % changed)
    logger.info('TELEGRAM_TOKEN: %s' % TELEGRAM_TOKEN)

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
    varKeys = [
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
    ]
    content = debugObj(obj, varKeys)
    res = Response(content)
    res.headers['Content-type'] = 'text/plain'
    return res
