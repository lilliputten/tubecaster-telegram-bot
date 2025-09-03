# -*- coding: utf-8 -*-
# vim: ft=python:
# @module WSGI Entrypoint
# @desc WSGI server start script
# @since 2024.11.27, 00:00
# @changed 2024.12.16, 11:23

# NOTE: Don't use the name of 'index.wsgi' for this file due to effects with vercel server (it returns it as a plain response on any request)

import os  # noqa

#  import pathlib
import sys  # noqa

# Server only params (start locally with dev-mode flask command, or `pnpm run dev`)...
venvRoot = '/var/www'
venv = '.venv-tubecaster'
venvActivateScript = 'bin/activate_this.py'

# Activate venv...
activateThis = os.path.join(venvRoot, venv, venvActivateScript)

with open(activateThis) as f:
    code = compile(f.read(), activateThis, 'exec')
    exec(code, dict(__file__=activateThis))

# Inject application path...
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
#  PROJECT_PATH = pathlib.Path(os.path.abspath(__file__)).as_posix()

sys.path.insert(1, PROJECT_PATH)  # noqa  # pylint: disable=wrong-import-position


# Start application...
from api.index import app as application

__all__ = ['application']

if __name__ == '__main__':
    application.run()
