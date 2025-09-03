# -*- coding:utf-8 -*-

import traceback
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from core.helpers.errors import errorToString
from core.logger import getDebugLogger
from core.logger.utils import errorStyle, primaryStyle, secondaryStyle, titleStyle, warningStyle

_logger = getDebugLogger()

_logTraceback = False


def testPydantic():
    try:

        class User(BaseModel):
            id: int
            name: str = 'John Doe'
            signup_ts: Optional[datetime] = None
            friends: List[int] = []

        external_data = {
            'id': '123',
            'signup_ts': '2017-06-01 12:22',
            'friends': [1, '2', b'3'],
        }

        user = User(**external_data)

        _logger.info('testPydantic: ' + repr(user))
        # > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]

        _logger.info('testPydantic: ' + repr(user.id))
        # > 123
    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'testPydantic: Error caught: ' + sError
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.warning(warningStyle('TtestPydantic: raceback for the following error:') + sTraceback)
        _logger.error(errorStyle(errMsg))


if __name__ == '__main__':
    testPydantic()
