# -*- coding:utf-8 -*-

import os
from dotenv import dotenv_values
import pathlib
import posixpath


CHANGED = """
@changed 2024.12.01, 01:28
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

# Module exports...
__all__ = [
    'appConfig',
]

if __name__ == '__main__':
    test = appConfig.get('TEST')
    print('main %s' % test)
