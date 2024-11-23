import logging

# Setup format
nameWidth = 20
nameFormat = '-' + str(nameWidth) + 's'

# Show time in log data
showTime = False

# Level (TODO: Make derived from a dev or prod environment?)
loggingLevel = logging.DEBUG

formatStr = ' '.join(
    list(
        filter(
            None,
            [
                # Combine log format string from items...
                '%(asctime)s' if showTime else None,
                '%(levelname)-8s',
                '%(name)' + nameFormat + '',
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
    return logger


# Module exports...
__all__ = [
    #  'logger',
    'getLogger',
]
