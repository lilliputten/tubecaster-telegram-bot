# -*- coding:utf-8 -*-

import logging

from core.appConfig import appConfig

# @see https://habr.com/ru/companies/wunderfund/articles/683880/
# @see https://docs.python.org/3/library/logging


LOCAL = appConfig.get('LOCAL')

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


def getLogger(id: str | None = None):
    logger = logging.getLogger(id)
    if not LOCAL:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(loggingLevel)
        logger.addHandler(console_handler)
    return logger


# Module exports...
__all__ = [
    #  'logger',
    'getLogger',
]
