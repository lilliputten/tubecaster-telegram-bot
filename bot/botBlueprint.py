# -*- coding:utf-8 -*-
from flask import Blueprint

from core.appConfig import appConfig
from core.logger import getLogger


logger = getLogger('bot/botBlueprint')

botBlueprint = Blueprint('botBlueprint', __name__)


@botBlueprint.route('/test')
def botBlueprint_test():
    """
    render_template demo
    """
    TELEGRAM_TOKEN = appConfig.get('TELEGRAM_TOKEN')
    logger.debug('botBlueprint_test %s' % TELEGRAM_TOKEN)
    #  return render_template('test.html')
    return 'Test route'


# Module exports...
__all__ = [
    'botBlueprint',
]
