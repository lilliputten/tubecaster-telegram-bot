# -*- coding:utf-8 -*-

import logging
import logging.handlers

from core.appConfig import appConfig

# @see https://habr.com/ru/companies/wunderfund/articles/683880/
# @see https://docs.python.org/3/library/logging

LOCAL = appConfig.get('LOCAL')

SYSLOG_FILE = appConfig.get('SYSLOG_FILE', 'pysyslog.log')
SYSLOG_HOST = appConfig.get('SYSLOG_HOST', '127.0.0.1')
SYSLOG_PORT = int(appConfig.get('SYSLOG_PORT', '514'))


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
                '%(name)' + nameFormat + '',
                '%(levelname)-8s',
                '%(message)s',
            ],
        )
    )
)

# @see https://habr.com/ru/companies/wunderfund/articles/683880/
logging.basicConfig(
    level=loggingLevel,
    format=formatStr,
    #  filename="py_log.log", filemode="w",
)


defaultFormatter = logging.Formatter(formatStr)


def getLogger(id: str | None = None):
    logger = logging.getLogger(id)
    # Syslog, @see https://docs.python.org/3/library/logging.handlers.html#sysloghandler
    syslogHandler = logging.handlers.SysLogHandler(
        address=(SYSLOG_HOST, SYSLOG_PORT),
    )
    syslogHandler.formatter = defaultFormatter
    logger.addHandler(syslogHandler)
    if not LOCAL:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(loggingLevel)
        logger.addHandler(consoleHandler)
    return logger


# Module exports...
__all__ = [
    #  'logger',
    'getLogger',
]
