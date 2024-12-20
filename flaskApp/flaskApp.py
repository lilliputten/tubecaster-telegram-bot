# -*- coding:utf-8 -*-

import traceback
from flask import Flask, g
from werkzeug.middleware.proxy_fix import ProxyFix

from core.appConfig import STATIC_PATH, isNormalRun
from core.helpers.errors import errorToString
from core.logger.logger import getDebugLogger

# from db import initDb, closeDb


_logger = getDebugLogger()

_logTraceback = False


def createFlaskApp():
    try:
        flaskApp: Flask = Flask(
            __name__,
            static_url_path='',
            static_folder=STATIC_PATH,
            # template_folder='web/templates', # TODO?
        )

        if isNormalRun:
            flaskApp.wsgi_app = ProxyFix(flaskApp.wsgi_app, x_host=1)

            # # Initialize prisma
            # with flaskApp.app_context():
            #     initDb(g)
            #
            # flaskApp.teardown_appcontext(closeDb)

        return flaskApp

    except Exception as err:
        sError = errorToString(err, show_stacktrace=False)
        sTraceback = str(traceback.format_exc())
        errMsg = 'createFlaskApp: Error caught: ' + sError
        if _logTraceback:
            errMsg += sTraceback
        else:
            _logger.info('createFlaskApp: Traceback for the following error:' + sTraceback)
        _logger.error(errMsg)
        raise err


flaskApp: Flask = createFlaskApp()

# Module exports...
__all__ = [
    'flaskApp',
]
