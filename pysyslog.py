#!/usr/bin/env python

## Tiny Syslog Server in Python.
##
## This is a tiny syslog server that is able to receive UDP based syslog
## entries on a specified port and save them to a file.
## That's it... it does nothing else...
## There are a few configuration parameters.

#
# NO USER SERVICEABLE PARTS BELOW HERE...
#

import logging
import re
import socketserver

import os
from dotenv import dotenv_values

config = {
    **dotenv_values('.env'),
    **dotenv_values('.env.local'),
    **os.environ,  # override loaded values with environment variables
}

SYSLOG_FILE = config.get('SYSLOG_FILE', 'pysyslog.log')
SYSLOG_HOST = config.get('SYSLOG_HOST', '0.0.0.0')
SYSLOG_PORT = int(config.get('SYSLOG_PORT', '514'))

loggingLevel = logging.INFO

# @see https://habr.com/ru/companies/wunderfund/articles/683880/
logging.basicConfig(
    level=loggingLevel,
    format='%(message)s',
    #  datefmt="",
    filename=SYSLOG_FILE,
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
        print('Server starting on %s:%s (with file: %s)...' % (SYSLOG_HOST, SYSLOG_PORT, SYSLOG_FILE))
        server = socketserver.UDPServer((SYSLOG_HOST, SYSLOG_PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
        print('Server started')
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print('Crtl+C Pressed. Shutting down.')
