# -*- coding:utf-8 -*-
from flask import Blueprint

from core.flaskApp import flaskApp
from core.appConfig import appConfig


# @see https://flask.palletsprojects.com/en/stable/blueprints

publicSiteBlueprint = Blueprint('publicSiteBlueprint', __name__)


@publicSiteBlueprint.route('/')
def publicSiteBlueprint_root():
    """
    render_template demo
    """
    #  return render_template('root.html')
    return 'Site index %s' % appConfig.get('changed')


@publicSiteBlueprint.route('/project-info')
def static_file():
    print('project-info')
    return flaskApp.send_static_file('project-info.txt')


# Module exports...
__all__ = [
    'publicSiteBlueprint',
]
