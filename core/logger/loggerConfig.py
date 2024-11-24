# -*- coding:utf-8 -*-

import logging
import logging.handlers
import json

import requests
from requests.adapters import HTTPAdapter

from urllib3.util import Retry

from core.appConfig import appConfig
from core.logger.DebugLog import addDebugLog, useDebugLogs
from core.utils.stripHtml import stripHtml

LOCAL = appConfig.get('LOCAL')

USE_LOGS_SERVER = bool(appConfig.get('USE_LOGS_SERVER', False))
USE_SYSLOG_SERVER = bool(appConfig.get('USE_SYSLOG_SERVER', False))

LOGS_FILE = appConfig.get('LOGS_FILE', 'pysyslog.log')
SYSLOG_HOST = appConfig.get('SYSLOG_HOST', '127.0.0.1')
SYSLOG_PORT = int(appConfig.get('SYSLOG_PORT', '514'))

LOGS_SERVER_PREFIX = appConfig.get('LOGS_SERVER_PREFIX', 'http://')
LOGS_SERVER_HOST = appConfig.get('LOGS_SERVER_HOST', '127.0.0.1')
LOGS_SERVER_PORT = int(appConfig.get('LOGS_SERVER_PORT', '8514'))
LOGS_SERVER_RETRIES = int(appConfig.get('LOGS_SERVER_RETRIES', '0'))
#  LOGS_SERVER_TOKEN = appConfig.get('LOGS_SERVER_TOKEN', '') # Could be used to provide basic authentification

LOGS_SERVER_URL = LOGS_SERVER_PREFIX + LOGS_SERVER_HOST + ':' + str(LOGS_SERVER_PORT)

__all__ = [
    'LOCAL',
    'USE_LOGS_SERVER',
    'USE_SYSLOG_SERVER',
    'LOGS_FILE',
    'SYSLOG_HOST',
    'SYSLOG_PORT',
    'LOGS_SERVER_PREFIX',
    'LOGS_SERVER_HOST',
    'LOGS_SERVER_PORT',
    'LOGS_SERVER_RETRIES',
    #  'LOGS_SERVER_TOKEN',
    'LOGS_SERVER_URL',
]
