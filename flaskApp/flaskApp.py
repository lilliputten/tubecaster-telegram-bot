# -*- coding:utf-8 -*-

import os
import posixpath
import pathlib

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

_cwd = pathlib.Path(os.getcwd()).as_posix()
_staticPath = posixpath.join(_cwd, 'static')

flaskApp = Flask(
    __name__,
    static_url_path='',
    static_folder=_staticPath,
    # template_folder='web/templates', # TODO?
)

flaskApp.wsgi_app = ProxyFix(flaskApp.wsgi_app, x_host=1)

# Module exports...
__all__ = [
    'flaskApp',
]
