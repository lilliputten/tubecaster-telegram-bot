from flask import Flask

from core.appConfig import appConfig
from core.logger import logger
from core.flaskApp import app


@app.route('/')
def home():
    #  return app.send_static_file("project-info.txt")
    return 'Site index!'


@app.route('/about')
def about():
    return 'About route'


@app.route('/project-info')
def static_file():
    print('project-info')
    return app.send_static_file('project-info.txt')


if __name__ == '__main__':
    test = appConfig.get('DOMAIN')
    logger.debug('main %s' % test)
