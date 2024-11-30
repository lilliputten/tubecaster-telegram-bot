# -*- coding:utf-8 -*-

import posixpath

from core.appConfig import appConfig, STATIC_PATH

# Telegram token from env or vercel settings
TELEGRAM_TOKEN = str(appConfig.get('TELEGRAM_TOKEN', ''))

# Bot owner id
TELEGRAM_OWNER_ID = int(appConfig.get('TELEGRAM_OWNER_ID', '0'))

# Should be provided by vercel environment for production
VERCEL_URL = str(appConfig.get('VERCEL_URL', ''))
IS_VERCEL = True if VERCEL_URL else False

# Should be vds remote host name an ngrok relay link (for the local mode)
WEBHOOK_HOST = str(appConfig.get('WEBHOOK_HOST', '127.0.0.1'))

# Default bot route
WEBHOOK_PATH = str(appConfig.get('WEBHOOK_PATH', '/webhook'))  # Local route, see implementation in `botRoutes.py`

WEBHOOK_PREFIX = str(appConfig.get('WEBHOOK_PREFIX', 'https://'))

# Compose correct webhook fully-qualified url...
WEBHOOK_RESOLVED_HOST = VERCEL_URL if VERCEL_URL else WEBHOOK_HOST
WEBHOOK_URL = WEBHOOK_RESOLVED_HOST + WEBHOOK_PATH
if not WEBHOOK_URL.startswith('http'):
    WEBHOOK_URL = WEBHOOK_PREFIX + WEBHOOK_URL

# Images for show as a help and start banner
coverImagePath = posixpath.join(STATIC_PATH, 'img/bot-cover-640x360.jpg')
visualImagePath = posixpath.join(STATIC_PATH, 'img/bot-visual-640x360.jpg')
