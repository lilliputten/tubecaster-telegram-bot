#!/usr/bin/env python

import logging
import os
import re
import socketserver

from dotenv import dotenv_values

appConfig = {
    **dotenv_values('.env'),
    **dotenv_values('.env.local'),
    **os.environ,  # override loaded values with environment variables
}

LOGGING_SERRVER_LOG_FILE = appConfig.get('LOGGING_SERRVER_LOG_FILE', 'logging-server.log')

SYSLOG_HOST = appConfig.get('SYSLOG_HOST', '0.0.0.0')
SYSLOG_PORT = int(appConfig.get('SYSLOG_PORT', '514'))

loggingLevel = logging.INFO

# @see https://habr.com/ru/companies/wunderfund/articles/683880/
logging.basicConfig(
    level=loggingLevel,
    format='%(message)s',
    #  datefmt="",
    filename=LOGGING_SERRVER_LOG_FILE,
    filemode='a',
)


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        # socket = self.request[1]
        logStr = str(data).replace('\x00', '').strip()
        logStr = re.sub(r'^\s*(<\d+>)', r'\1 ', logStr)
        logStr = self.client_address[0] + ' ' + logStr
        print(logStr)
        logging.info(logStr)


if __name__ == '__main__':
    try:
        print('Server starting on %s:%s (with file: %s)...' % (SYSLOG_HOST, SYSLOG_PORT, LOGGING_SERRVER_LOG_FILE))
        server = socketserver.UDPServer((SYSLOG_HOST, SYSLOG_PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
        print('Server started')
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print('Crtl+C Pressed. Shutting down.')
