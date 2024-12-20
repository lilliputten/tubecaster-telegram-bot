# -*- coding:utf-8 -*-

from flask import Flask, g
from werkzeug.middleware.proxy_fix import ProxyFix

from core.appConfig import STATIC_PATH

flaskApp: Flask = Flask(
    __name__,
    static_url_path='',
    static_folder=STATIC_PATH,
    # template_folder='web/templates', # TODO?
)

flaskApp.wsgi_app = ProxyFix(flaskApp.wsgi_app, x_host=1)

# Module exports...
__all__ = [
    'flaskApp',
]
