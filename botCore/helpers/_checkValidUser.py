from core.logger.logger import getDebugLogger
from core.logger.utils import titleStyle
from db import findUser


_logger = getDebugLogger()


def checkValidUser(userId: int):
    user = findUser(userId)
    _logger.info(titleStyle(f'Found user: {user}'))
    return True if user is not None else False
