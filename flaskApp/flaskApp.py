# -*- coding:utf-8 -*-

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

flaskApp = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    # template_folder='web/templates', # TODO?
)

flaskApp.wsgi_app = ProxyFix(flaskApp.wsgi_app, x_host=1)

# Module exports...
__all__ = [
    'flaskApp',
]
