# -*- coding:utf-8 -*-

from core.appConfig import appConfig

TELEGRAM_TOKEN = appConfig.get('TELEGRAM_TOKEN')

VERCEL_URL = appConfig.get('VERCEL_URL', '')

WEBHOOK_PREFIX = appConfig.get('WEBHOOK_PREFIX', 'https://')
WEBHOOK_HOST = appConfig.get('WEBHOOK_HOST', '127.0.0.1')
WEBHOOK_PATH = appConfig.get('WEBHOOK_PATH', '/webhook')

WEBHOOK_RESOLVED_HOST = VERCEL_URL if VERCEL_URL else WEBHOOK_HOST
WEBHOOK_URL = WEBHOOK_PREFIX + WEBHOOK_RESOLVED_HOST + WEBHOOK_PATH
