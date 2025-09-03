# -*- coding:utf-8 -*-

import posixpath

from core.appConfig import STATIC_PATH, VERCEL_URL, appConfig

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
