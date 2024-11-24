# -*- coding:utf-8 -*-

import logging
import logging.handlers
import json

#  import re
import requests
from requests.adapters import HTTPAdapter

#  from requests.packages.urllib3.util.retry import Retry
from urllib3.util import Retry

from core.appConfig import appConfig
from core.utils.stripHtml import stripHtml

# @see https://habr.com/ru/companies/wunderfund/articles/683880/
# @see https://docs.python.org/3/library/logging

LOCAL = appConfig.get('LOCAL')

USE_LOGS_SERVER = bool(appConfig.get('USE_LOGS_SERVER', True))
USE_SYSLOG_SERVER = bool(appConfig.get('USE_SYSLOG_SERVER', False))

LOGS_FILE = appConfig.get('LOGS_FILE', 'pysyslog.log')
SYSLOG_HOST = appConfig.get('SYSLOG_HOST', '127.0.0.1')
SYSLOG_PORT = int(appConfig.get('SYSLOG_PORT', '514'))

LOGS_SERVER_PREFIX = appConfig.get('LOGS_SERVER_PREFIX', 'http://')
LOGS_SERVER_HOST = appConfig.get('LOGS_SERVER_HOST', '127.0.0.1')
LOGS_SERVER_PORT = int(appConfig.get('LOGS_SERVER_PORT', '8514'))
LOGS_SERVER_RETRIES = int(appConfig.get('LOGS_SERVER_RETRIES', '0'))
#  LOGS_SERVER_TOKEN = appConfig.get('LOGS_SERVER_TOKEN', '')

LOGS_SERVER_URL = LOGS_SERVER_PREFIX + LOGS_SERVER_HOST + ':' + str(LOGS_SERVER_PORT)

# Setup format
nameWidth = 20
nameFormat = '-' + str(nameWidth) + 's'

# Show time in log data
showTime = False

# Level (TODO: Make derived from a dev or prod environment?)
loggingLevel = logging.INFO   # DEBUG

formatStr = ' '.join(
    list(
        filter(
            None,
            [
                # Combine log format string from items...
                '%(asctime)s' if showTime else None,
                '%(name)' + nameFormat,
                '%(levelname)-8s',
                '%(message)s',
            ],
        )
    )
)

debugLogs: list[str] = []


def getDebugLog():
    return '\n' + '\n'.join(debugLogs) + '\n'


class CustomHttpHandler(logging.Handler):
    def __init__(
        self,
        url: str,
        #  token: str,
        silent: bool = True,
    ):
        """
        Initializes the custom http handler
        Parameters:
            url (str): The URL that the logs will be sent to
            token (str): The Authorization token being used
            silent (bool): If False the http response and logs will be sent
            to STDOUT for debug
        """
        self.url = url
        #  self.token = token
        self.silent = silent

        debugLogs.append('CustomHttpHandler url: %s' % (url))

        # sets up a session with the server
        self.MAX_POOLSIZE = 100
        self.session = session = requests.Session()
        session.headers.update(
            {
                'Content-Type': 'application/json',
                #  'Authorization': 'Bearer %s' % (self.token)
            }
        )
        self.session.mount(
            #  'https://',
            LOGS_SERVER_PREFIX,
            HTTPAdapter(
                max_retries=Retry(total=LOGS_SERVER_RETRIES, backoff_factor=0.5, status_forcelist=[403, 500]),
                pool_connections=self.MAX_POOLSIZE,
                pool_maxsize=self.MAX_POOLSIZE,
            ),
        )

        super().__init__()

    def emit(self, record):
        """
        This function gets called when a log event gets emitted. It recieves a
        record, formats it and sends it to the url
        Parameters:
            record: a log record
        """
        sendData = self.format(record)
        #  jsonData = {
        #      'asctime': record.asctime,
        #      'pathname': record.pathname,
        #      'lineno': record.lineno,
        #      'name': record.name,
        #      'levelname': record.levelname,
        #      'message': record.message,
        #  }
        debugLogs.append('emit %s %s %s %s' % (self.url, record.name, record.levelname, record.message))
        try:
            url = self.url
            response = self.session.post(url, data=sendData)
            #  response = requests.post(url, json=jsonData)
            resp = response.content.decode('utf-8')
            resp = stripHtml(resp)
            debugLogs.append('emit result: %s' % (resp))
            if not self.silent:
                print(sendData)
                print(response.content)
        except Exception as err:
            debugLogs.append('emit error: %s' % (repr(err)))
            print('ERROR: Failed to send a log record:', repr(err))
            # TODO: Stop sending logs after a few errors?


# Create remote server log formatter - this formats the log messages accordingly
remoteLoggingFormatter = logging.Formatter(
    json.dumps(
        {
            'asctime': '%(asctime)s',
            'pathname': '%(pathname)s',
            'lineno': '%(lineno)d',
            'name': '%(name)s',
            'levelname': '%(levelname)s',
            'message': '%(message)s',
        }
    )
)

# Create a custom http logger handler
httpHandler = CustomHttpHandler(
    url=LOGS_SERVER_URL,
    #  token=LOGS_SERVER_TOKEN,
    #  silent=False,
)
httpHandler.setLevel(loggingLevel)
httpHandler.setFormatter(remoteLoggingFormatter)

# Remove default handlers...
logging.getLogger().handlers.clear()

# @see https://habr.com/ru/companies/wunderfund/articles/683880/
logging.basicConfig(
    level=loggingLevel,
    format=formatStr,
    #  filename="py_log.log", filemode="w",
)

defaultFormatter = logging.Formatter(formatStr)


def getLogger(id: str | None = None):
    logger = logging.getLogger(id)
    #  debugLogs.append('getLogger loggers count: %d' % (len(logger.handlers)))
    #  if len(logger.handlers):
    #      logger.removeHandler(logger.handlers[0])
    # Default handler (console)...
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(loggingLevel)
    consoleHandler.formatter = defaultFormatter
    #  logger.handlers = []
    #  logger.addHandler(consoleHandler)
    # Syslog, @see https://docs.python.org/3/library/logging.handlers.html#sysloghandler
    if USE_SYSLOG_SERVER:
        syslogHandler = logging.handlers.SysLogHandler(
            address=(SYSLOG_HOST, SYSLOG_PORT),
        )
        syslogHandler.setLevel(loggingLevel)
        syslogHandler.formatter = defaultFormatter
        logger.addHandler(syslogHandler)
    debugLogs.append('getLogger %s USE_LOGS_SERVER: %s' % (id, USE_LOGS_SERVER))
    if USE_LOGS_SERVER:
        logger.addHandler(httpHandler)
    return logger


# Module exports...
__all__ = [
    #  'logger',
    'getLogger',
]
