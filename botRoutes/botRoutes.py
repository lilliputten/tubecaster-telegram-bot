# -*- coding:utf-8 -*-

from flask import Blueprint

#  from core.appConfig import PROJECT_INFO

from core.logger import getDebugLogger
from core.utils import debugObj

from botCore.botConfig import WEBHOOK_URL


# Create a blueprint route
botRoutes = Blueprint('botRoutes', __name__)

_logger = getDebugLogger()


def showDebug():
    """
    Debug: Show blueprint routes start info.
    """
    debugItems = {
        #  'PROJECT_INFO': PROJECT_INFO,
        'WEBHOOK_URL': WEBHOOK_URL,
    }
    logItems = [
        'botRoute: Blueprint routes started',
        debugObj(debugItems),
    ]
    logContent = '\n'.join(logItems)
    _logger.info(logContent)


# DEBUG
showDebug()


# Module exports...
__all__ = [
    'botRoutes',
]
