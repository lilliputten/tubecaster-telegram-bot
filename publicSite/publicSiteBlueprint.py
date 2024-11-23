# -*- coding:utf-8 -*-
from flask import Blueprint

from core.appConfig import appConfig

#  from core.logger import logger


publicSiteBlueprint = Blueprint('publicSiteBlueprint', __name__)


@publicSiteBlueprint.route('/')
def publicSiteBlueprint_root():
    """
    render_template demo
    """
    #  logger.debug('publicSiteBlueprint_root')
    #  return render_template('root.html')
    return 'Site index'


# Module exports...
__all__ = [
    'publicSiteBlueprint',
]
