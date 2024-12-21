# -*- coding:utf-8 -*-

import logging
import logging.handlers
import re

from core.helpers.strings import removeAnsiStyles
from core.helpers.time import getTimeStamp
from core.logger import loggerConfig


class NoColorFormatter(logging.Formatter):
    """
    Log formatter that strips terminal colour
    escape codes from the log message.
    """

    def format(self, record):
        """Return logger message with terminal escapes removed."""
        data = record.__dict__
        data['asctime'] = getTimeStamp('precise')
        data['message'] = removeAnsiStyles(record.msg)
        return loggerConfig.formatStr % data
