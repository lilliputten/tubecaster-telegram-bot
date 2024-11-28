# -*- coding: utf-8 -*-
# vim: ft=python:
# @module index.wsgi
# @desc Fullspace hosting server start script
# @since 2024.11.27, 00:00
# @changed 2024.11.28, 01:49

import sys  # noqa
import os  # noqa

venv = '.venv-default'

# Server only params (start locally with dev-mode flask command, or `pnpm run dev`)...
venvRoot = '/var/www'
venvActivateScript = 'bin/activate_this.py'
venvActivateLocal = 'Scripts/activate_this.py'
# TODO: Check if it's server or local run?

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

