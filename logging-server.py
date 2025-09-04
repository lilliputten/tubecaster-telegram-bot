#!/usr/bin/env python

"""

This server allows to collect remote logs from the vercel hosted application via http protocol.

Use ngrok to expose a local server to the remote app. See `.env.local.SAMPLE` as an example of remote settings.

See environment variable to configure it:

- LOGGING_SERRVER_LOG_FILE
- LOGS_SERVER_PREFIX
- LOGS_SERVER_HOST
- LOGS_SERVER_PORT
- LOGS_SERVER_RETRIES
"""

import json
import logging
import os
import pathlib
import posixpath
import sys
from contextlib import contextmanager

#  from dotenv import dotenv_values
from http.server import BaseHTTPRequestHandler, HTTPServer

from concurrent_log_handler import ConcurrentRotatingFileHandler

from core.helpers.time import getTimeStamp
from core.logger import loggerConfig
from core.logger.NoColorFormatter import NoColorFormatter

#  _appConfig = {
#      **dotenv_values('.env'),
#      **dotenv_values('.env.local'),
#      **os.environ,  # override loaded values with environment variables
#  }

_useLocalLogFile = True

# Trick to hide server logs: hide stderr output (requires extra attention to handle errors)
_showRequestsLog = False

# Show specific parameters...
_showIp = False  # It's always a localhost (if working via ngrok)
_showFile = False
_showTime = True

# Setup format
_nameWidth = 20
_nameFormat = '-' + str(_nameWidth) + 's'
_fileWidth = 80
_fileFormat = '-' + str(_fileWidth) + 's'

# Level (TODO: Make derived from a dev or prod environment?)
_loggingLevel = logging.INFO   # DEBUG

_localLogFormat = '%(message)s'
_localFormatter = logging.Formatter(_localLogFormat)

_noColorFormatter = NoColorFormatter()

# Format for re-create remote log string (local data won't be included into the output)
formatStr = ' '.join(
    list(
        filter(
            None,
            [
                # Combine log format string from items...
                #  '%(pathname)', # .../api/index.py (full pathname)
                #  '%(lineno)', # 30
                '%(file)' + _fileFormat if _showFile else None,  # pathname:lineno
                '%(ip)s' if _showIp else None,
                '%(asctime)s' if _showTime else None,  # 2024-11-24 05:41:29,110
                '%(name)' + _nameFormat,  # api/index
                '%(levelname)-8s',  # INFO
                '%(message)s',  # Start: 2024.11.24, 01:18
            ],
        )
    )
)

# @see https://habr.com/ru/companies/wunderfund/articles/683880/
logging.basicConfig(
    level=_loggingLevel,
    format=_localLogFormat,
    #  datefmt="",
    filename=loggerConfig.LOGGING_SERRVER_LOG_FILE,
    filemode='a',
)


@contextmanager
def suppress_stderr():
    """
    Suppress stderr logging messages (requests info).
    """
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        if not _showRequestsLog:
            sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.silent = True
        self._http_server_logger_enabled = False
        super().__init__(request, client_address, server)
        self.silent = True
        self._http_server_logger_enabled = False

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        errStr = 'Expecting POST method'
        self.wfile.write(errStr.encode('utf-8'))
        print(errStr)

    def do_POST(self):
        self._set_response()
        contentType = self.headers.get('Content-Type', 'unknown')
        ip = self.request.getpeername()[0]
        if not contentType.startswith('application/json'):
            errStr = 'Expecting json data, but got %s' % contentType
            self.wfile.write(errStr.encode('utf-8'))
            print(errStr)
            raise Exception(errStr)
        contentLength = int(self.headers.get('Content-Length', '0'))
        # Parse json...
        try:
            jsonStr = self.rfile.read(contentLength).decode('utf-8')
            data = json.loads(jsonStr)
            # Prepare data...
            data['pathname'] = data.get('pathname', '').replace('\\', '/')
            if data.get('pathname') and data.get('lineno'):
                data['file'] = data.get('pathname', '') + ':' + str(data.get('lineno', ''))
            data['ip'] = ip
            #  Sample: api/index            INFO     Start: 2024.11.24, 01:18
            logStr = formatStr % data
            #  print(logStr)
            logger.info(logStr)
            timeStr = getTimeStamp()
            response = 'OK ' + timeStr
            # print('Result: ' + response)
            self.wfile.write(response.encode('utf-8'))
        except Exception as err:
            errStr = 'Error parsing log data: ' + repr(err)
            self.wfile.write(errStr.encode('utf-8'))
            print(errStr)
            raise Exception(errStr)


def initLocalLogger(id: str | None = None):
    logger = logging.getLogger(id)
    # Default handler (console)...
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(_loggingLevel)
    consoleHandler.formatter = _localFormatter
    logger.addHandler(consoleHandler)
    # Local file handler...
    if _useLocalLogFile:
        cwd = pathlib.Path(os.getcwd()).as_posix()
        localLogFileHandler = ConcurrentRotatingFileHandler(
            # @see:
            # - https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler
            # - [logging - Rotating file handler gives error in python logw](https://stackoverflow.com/questions/68253737/rotating-file-handler-gives-error-in-python-log/77394567#77394567)
            filename=posixpath.join(cwd, loggerConfig.LOGGING_SERRVER_LOG_FILE),
            mode='a',
            encoding='utf-8',
            maxBytes=100000,
            backupCount=5,
            #  delay=True,
            #  errors=True,
        )  # max log file size 100 MB
        localLogFileHandler.setFormatter(_noColorFormatter)
        localLogFileHandler.setLevel(_loggingLevel)
        localLogFileHandler.formatter = _noColorFormatter
        localLogFileHandler.level = _loggingLevel
        logger.addHandler(localLogFileHandler)
    return logger


def run(ServerClass=HTTPServer, HandlerClass=RequestHandler, port=loggerConfig.LOGS_SERVER_PORT):
    serverAddress = ('', port)
    httpd = ServerClass(serverAddress, HandlerClass)
    try:
        # NOTE: Disable request logging (server.py: `sys.stderr.write(...)`)
        with suppress_stderr():
            httpd.serve_forever()
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print('Crtl+C Pressed. Shutting down.')
    httpd.server_close()


# Remove default handlers...
logging.getLogger().handlers.clear()

logger = initLocalLogger('logging-server')
logger.info('OK')

if __name__ == '__main__':
    print(
        'Server is running on %s:%s (with file: %s)...'
        % (loggerConfig.LOGS_SERVER_HOST, loggerConfig.LOGS_SERVER_PORT, loggerConfig.LOGGING_SERRVER_LOG_FILE)
    )
    try:
        # Initialize local logger...
        # Start...
        run()
    except Exception as err:
        print('ERROR:', repr(err))
    print('Server stopped')
