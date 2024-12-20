#!/bin/sh
# @desc Installing all requierements (under venv)
# @changed 2024.12.19, 23:11

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`

test -f "$scriptsPath/check-venv.sh" && . "$scriptsPath/check-venv.sh"

echo "Installing all requierements (under venv)..." \
&& pip install -r requirements.txt \
&& echo "OK"
