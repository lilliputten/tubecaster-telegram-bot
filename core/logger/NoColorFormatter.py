# -*- coding:utf-8 -*-

import logging
import logging.handlers
import re

from core.helpers.time import getTimeStamp
from core.logger import loggerConfig

class NoColorFormatter(logging.Formatter):
    """
    Log formatter that strips terminal colour
    escape codes from the log message.
    """

    # Regex for ANSI colour codes
    ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

    def format(self, record):
        """Return logger message with terminal escapes removed."""
        data = record.__dict__
        data['asctime'] = getTimeStamp('precise')
        data['message'] = re.sub(self.ANSI_RE, "", record.msg)
        return loggerConfig.formatStr % data
