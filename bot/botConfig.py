# -*- coding:utf-8 -*-

from core.appConfig import appConfig

TELEGRAM_TOKEN = appConfig.get('TELEGRAM_TOKEN')  # Telegram token from env or vercel settings

VERCEL_URL = appConfig.get('VERCEL_URL', '')  # Should be provided by vercel environment for production

WEBHOOK_PREFIX = appConfig.get('WEBHOOK_PREFIX', 'https://')
WEBHOOK_HOST = appConfig.get('WEBHOOK_HOST', '127.0.0.1')  # Should be an ngrok relay link (for the local mode)
WEBHOOK_PATH = appConfig.get('WEBHOOK_PATH', '/webhook')  # Local route, see implementation in `botBlueprint.py`

# Compose correct webhook fully-qualified url...
WEBHOOK_RESOLVED_HOST = VERCEL_URL if VERCEL_URL else WEBHOOK_HOST
WEBHOOK_URL = WEBHOOK_RESOLVED_HOST + WEBHOOK_PATH
if not WEBHOOK_URL.startswith('http'):
    WEBHOOK_URL = WEBHOOK_PREFIX + WEBHOOK_URL
