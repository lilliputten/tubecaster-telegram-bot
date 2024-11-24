#!/usr/bin/env python

"""

This server allows to collect remote logs from the vercel hosted application via http protocol.

Use ngrok to expose a local server to the remote app. See `.env.local.SAMPLE` as an example of remote settings.

See environment variable to configure it:

- LOGS_FILE
- LOGS_SERVER_PREFIX
- LOGS_SERVER_HOST
- LOGS_SERVER_PORT
- LOGS_SERVER_RETRIES
"""

import logging

from datetime import datetime

import json
import os
from dotenv import dotenv_values
from http.server import BaseHTTPRequestHandler, HTTPServer
from contextlib import contextmanager
import sys

from core.utils.sanityJson import sanityJson

appConfig = {
    **dotenv_values('.env'),
    **dotenv_values('.env.local'),
    **os.environ,  # override loaded values with environment variables
}

LOGS_FILE = appConfig.get('LOGS_FILE', 'logs-server.log')

LOGS_SERVER_PREFIX = appConfig.get('LOGS_SERVER_PREFIX', 'http://')
LOGS_SERVER_HOST = appConfig.get('LOGS_SERVER_HOST', '0.0.0.0')
LOGS_SERVER_PORT = int(appConfig.get('LOGS_SERVER_PORT', '8514'))
LOGS_SERVER_RETRIES = int(appConfig.get('LOGS_SERVER_RETRIES', '0'))
#  LOGS_SERVER_TOKEN = appConfig.get('LOGS_SERVER_TOKEN', '') # TODO: It's possible to add basic authentification

LOGS_SERVER_URL = LOGS_SERVER_PREFIX + LOGS_SERVER_HOST + ':' + str(LOGS_SERVER_PORT)

showRequestsLog = True

# Show specific parameters...
showIp = False  # It's always a localhost (if working via ngrok)
showFile = False
showTime = True

# Setup format
nameWidth = 20
nameFormat = '-' + str(nameWidth) + 's'
fileWidth = 80
fileFormat = '-' + str(fileWidth) + 's'

# Level (TODO: Make derived from a dev or prod environment?)
loggingLevel = logging.CRITICAL   # DEBUG

formatStr = ' '.join(
    list(
        filter(
            None,
            [
                # Combine log format string from items...
                #  '%(pathname)', # .../api/index.py (full pathname)
                #  '%(lineno)', # 30
                '%(ip)s' if showIp else None,
                '%(file)' + fileFormat if showFile else None,  # pathname:lineno
                '%(asctime)s' if showTime else None,  # 2024-11-24 05:41:29,110
                '%(name)' + nameFormat,  # api/index
                '%(levelname)-8s',  # INFO
                '%(message)s',  # Start: 2024.11.24, 01:18
            ],
        )
    )
)


# @see https://habr.com/ru/companies/wunderfund/articles/683880/
logging.basicConfig(
    level=loggingLevel,
    format='%(message)s',
    #  datefmt="",
    filename=LOGS_FILE,
    filemode='a',
)


@contextmanager
def suppress_stderr():
    """
    Suppress stderr logging messages (requests info).
    """
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        if not showRequestsLog:
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
            jsonStr = sanityJson(jsonStr)
            data = json.loads(jsonStr)
            # Prepare data...
            data['pathname'] = data.get('pathname', '').replace('\\', '/')
            data['file'] = data.get('pathname', '') + ':' + str(data.get('lineno', ''))
            data['ip'] = ip
            #  Sample: api/index            INFO     Start: 2024.11.24, 01:18
            logStr = formatStr % data
            print(logStr)
            logging.info(logStr)
            timeStr = datetime.today().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
            response = 'OK ' + timeStr
            print('Result: ' + response)
            self.wfile.write(response.encode('utf-8'))
        except Exception as err:
            errStr = 'Error parsing log data: ' + repr(err)
            self.wfile.write(errStr.encode('utf-8'))
            print(errStr)
            raise Exception(errStr)


def run(ServerClass=HTTPServer, HandlerClass=RequestHandler, port=LOGS_SERVER_PORT):
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


if __name__ == '__main__':
    print('Server is running on %s:%s (with file: %s)...' % (LOGS_SERVER_HOST, LOGS_SERVER_PORT, LOGS_FILE))
    try:
        run()
    except Exception as err:
        print('ERROR:', repr(err))
    print('Server stopped')
