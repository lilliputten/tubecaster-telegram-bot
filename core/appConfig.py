# -*- coding:utf-8 -*-

import os
from dotenv import dotenv_values
import pathlib
import posixpath


CHANGED = """
@changed 2024.12.17, 10:45
""".strip().replace(
    '@changed ', ''
)

PROJECT_PATH = pathlib.Path(os.getcwd()).as_posix()
STATIC_PATH = posixpath.join(PROJECT_PATH, 'static')

PROJECT_INFO = CHANGED
with open(posixpath.join(STATIC_PATH, 'project-info.txt')) as fh:
    info = fh.read()
    if info:
        PROJECT_INFO = info.strip()

appConfig = {
    # Basic environment variables
    **dotenv_values('.env'),
    # Real telegram webhook address for the real deploy server
    **dotenv_values('.env.server'),
    # Local flask server tunneled for telegram webhook access and LOCAL flag
    **dotenv_values('.env.local'),
    # Secure parameters for telebot and yt-dlp
    **dotenv_values('.env.secure'),
    # Logging server ngrok tunnel address
    **dotenv_values('.env.logging-ngrok'),
    # Override loaded values with environment variables
    **os.environ,
    # Other parameters
    **{
        # Project info
        'CHANGED': CHANGED,
        # DEBUG: Changed timestamp
        'PROJECT_INFO': PROJECT_INFO,
        # Paths...
        'PROJECT_PATH': PROJECT_PATH,
        'STATIC_PATH': STATIC_PATH,
    },
}

LOCAL = bool(appConfig.get('LOCAL'))
WERKZEUG_RUN_MAIN = bool(appConfig.get('WERKZEUG_RUN_MAIN'))
isNormalRun = not LOCAL or WERKZEUG_RUN_MAIN

AUDIO_FILE_EXT = str(appConfig.get('AUDIO_FILE_EXT', '.mp3'))

# Timezone (set `TZ_HOURS` to hours value to adjust date representation to corresponding timezone)
TZ_HOURS = appConfig.get('TZ_HOURS_OFFSET')

# Tg params...
TELEGRAM_TOKEN = str(appConfig.get('TELEGRAM_TOKEN', ''))
TELEGRAM_OWNER_ID = int(appConfig.get('TELEGRAM_OWNER_ID', '0'))
LOGGING_CHANNEL_ID = str(appConfig.get('LOGGING_CHANNEL_ID', ''))

# Should be provided by vercel environment for production
VERCEL_URL = str(appConfig.get('VERCEL_URL', ''))
IS_VERCEL = True if VERCEL_URL else False

# Current root project path
CWD_PATH = PROJECT_PATH  # pathlib.Path(os.getcwd()).as_posix()

# Temp path: Use local 'temp' or vercel specific '/tmp' folders for temporary files
TEMP_PATH = posixpath.join(CWD_PATH, '.temp') if LOCAL or not IS_VERCEL else '/tmp'

# Audio...

# Max audio file size for tg bot, in bytes
# @see https://core.telegram.org/bots/faq#how-do-i-upload-a-large-file
MAX_AUDIO_FILE_SIZE = int(appConfig.get('MAX_AUDIO_FILE_SIZE', '50000000'))


if __name__ == '__main__':
    test = appConfig.get('TEST')
    print('main %s' % test)
