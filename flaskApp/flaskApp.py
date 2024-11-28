# -*- coding:utf-8 -*-

from flask import Flask

flaskApp = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    # template_folder='web/templates', # TODO?
)

# Module exports...
__all__ = [
    'flaskApp',
]
