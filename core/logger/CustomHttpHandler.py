# -*- coding:utf-8 -*-

import logging
import logging.handlers
import json

import requests
from requests.adapters import HTTPAdapter

from urllib3.util import Retry

from core.logger.DebugLog import addDebugLog, useDebugLogs
from core.logger import loggerConfig
from core.utils.stripHtml import stripHtml


# @see https://habr.com/ru/companies/wunderfund/articles/683880/
# @see https://docs.python.org/3/library/logging


def prepareJson(s: str):
    return s


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

        # if useDebugLogs:
        #     addDebugLog('CustomHttpHandler url: %s' % (url))

        # sets up a session with the server
        self.MAX_POOLSIZE = 100
        self.session = session = requests.Session()
        session.headers.update(
            {
                'Content-Type': 'application/json',
                #  'Authorization': 'Bearer %s' % (self.token),
            }
        )
        self.session.mount(
            loggerConfig.LOGS_SERVER_PREFIX,
            HTTPAdapter(
                max_retries=Retry(
                    total=loggerConfig.LOGS_SERVER_RETRIES, backoff_factor=0.5, status_forcelist=[403, 500]
                ),
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
        sendData = self.format(record)  # NOTE: This isn't a valid json format
        logData = {
            'asctime': record.asctime,
            'pathname': record.pathname,
            'lineno': record.lineno,
            'name': record.name,
            'levelname': record.levelname,
            'message': record.message,
        }
        jsonData = json.dumps(logData)
        if useDebugLogs:
            addDebugLog(
                'logger:CustomHttpHandler:emit %s %s %s %s' % (self.url, record.name, record.levelname, record.message)
            )
        try:
            url = self.url
            response = self.session.post(url, data=jsonData)
            #  response = self.session.post(url, data=sendData)
            resp = response.content.decode('utf-8')
            resp = stripHtml(resp)
            addDebugLog('logger:CustomHttpHandler:emit result: %s' % (resp))
            if not self.silent:
                print(sendData)
                print(response.content)
        except Exception as err:
            if useDebugLogs:
                addDebugLog('logger:CustomHttpHandler:emit error: %s' % (repr(err)))
            print('ERROR: Failed to send a log record:', repr(err))
            # TODO: Stop sending logs after a few errors?


# Create remote server log formatter - this formats the log messages accordingly
customHttpHandlerFormatter = logging.Formatter(
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


# Module exports...
__all__ = [
    'CustomHttpHandler',
    'customHttpHandlerFormatter',
]
