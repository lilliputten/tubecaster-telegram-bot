# -*- coding:utf-8 -*-
from flask import Blueprint

from core.appConfig import appConfig


# @see https://flask.palletsprojects.com/en/stable/blueprints

publicSiteBlueprint = Blueprint('publicSiteBlueprint', __name__)


@publicSiteBlueprint.route('/')
def publicSiteBlueprint_root():
    """
    render_template demo
    """
    #  return render_template('root.html')
    return 'Site index'


# Module exports...
__all__ = [
    'publicSiteBlueprint',
]
