# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import Response
from datetime import datetime

from core.logger import getLogger
from core.flaskApp import flaskApp
from core.appConfig import appConfig


logger = getLogger('publicSite/publicSiteBlueprint')

# @see https://flask.palletsprojects.com/en/stable/blueprints

publicSiteBlueprint = Blueprint('publicSiteBlueprint', __name__)


@publicSiteBlueprint.route('/')
def publicSiteBlueprint_root():
    """
    render_template demo
    """
    #  return render_template('root.html')
    timeStr = datetime.today().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
    testStr = 'ROOT ' + timeStr
    logger.info(testStr)
    res = Response(testStr)
    res.headers['Content-type'] = 'text/plain'
    return res


@publicSiteBlueprint.route('/project-info')
def static_file():
    print('project-info')
    return flaskApp.send_static_file('project-info.txt')
