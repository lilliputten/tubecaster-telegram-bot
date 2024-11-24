# -*- coding:utf-8 -*-

from core.appConfig import appConfig

TELEGRAM_TOKEN = appConfig.get('TELEGRAM_TOKEN')

WEBHOOK_HOST = appConfig.get('WEBHOOK_HOST', 'http://127.0.0.1')
WEBHOOK_PATH = appConfig.get('WEBHOOK_PATH', '/webhook')
