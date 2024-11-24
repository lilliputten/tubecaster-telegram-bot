# -*- coding:utf-8 -*-

import logging
import logging.handlers

from core.logger import loggerConfig
from core.logger.CustomHttpHandler import CustomHttpHandler, customHttpHandlerFormatter

# @see https://habr.com/ru/companies/wunderfund/articles/683880/
# @see https://docs.python.org/3/library/logging

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


# Create a custom http logger handler
httpHandler = CustomHttpHandler(
    url=loggerConfig.LOGS_SERVER_URL,
    #  token=LOGS_SERVER_TOKEN,
    #  silent=False,
)
httpHandler.setLevel(loggingLevel)
httpHandler.setFormatter(customHttpHandlerFormatter)

# Remove default handlers...
logging.getLogger().handlers.clear()

# @see https://habr.com/ru/companies/wunderfund/articles/683880/
logging.basicConfig(
    level=loggingLevel,
    format=formatStr,
)

defaultFormatter = logging.Formatter(formatStr)


def getLogger(id: str | None = None):
    logger = logging.getLogger(id)
    # Default handler (console)...
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(loggingLevel)
    consoleHandler.formatter = defaultFormatter
    # Syslog, @see https://docs.python.org/3/library/logging.handlers.html#sysloghandler
    if loggerConfig.USE_SYSLOG_SERVER:
        syslogHandler = logging.handlers.SysLogHandler(
            address=(loggerConfig.SYSLOG_HOST, loggerConfig.SYSLOG_PORT),
        )
        syslogHandler.setLevel(loggingLevel)
        syslogHandler.formatter = defaultFormatter
        logger.addHandler(syslogHandler)
    # if useDebugLogs:
    #     addDebugLog('getLogger %s USE_LOGS_SERVER: %s' % (id, USE_LOGS_SERVER))
    if loggerConfig.USE_LOGS_SERVER:
        logger.addHandler(httpHandler)
    return logger


# Module exports...
__all__ = [
    'getLogger',
]
