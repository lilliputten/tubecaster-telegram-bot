#!/bin/sh
# @desc Run python tests
# @changed 2024.12.20, 00:49

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`

test -f "$scriptsPath/check-venv.sh" && . "$scriptsPath/check-venv.sh"

echo "Run python tests..." && \
  python -m unittest discover -v -f -t . -s . -p *_test.py && \
  echo OK
