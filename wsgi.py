# -*- coding: utf-8 -*-
# vim: ft=python:
# @module WSGI Entrypoint
# @desc WSGI server start script
# @since 2024.11.27, 00:00
# @changed 2024.12.09, 02:01

# NOTE: Don't use the name of 'index.wsgi' for this file due to effects with vercel server (it returns it as a plain response on any request)

import sys  # noqa
import os  # noqa

venv = '.venv-default'

# Server only params (start locally with dev-mode flask command, or `pnpm run dev`)...
venvRoot = '/var/www'
venvActivateScript = 'bin/activate_this.py'

# Activate venv...
activateThis = os.path.join(venvRoot, venv, venvActivateScript)

with open(activateThis) as f:
    code = compile(f.read(), activateThis, 'exec')
    exec(code, dict(__file__=activateThis))

# Inject application path...
rootPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, rootPath)  # noqa  # pylint: disable=wrong-import-position


# Start application...
from api.index import app as application

__all__ = ['application']

if __name__ == '__main__':
    application.run()
