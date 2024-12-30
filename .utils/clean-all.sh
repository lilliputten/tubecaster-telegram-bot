#!/bin/sh
# @desc Clean all temp files
# @changed 2024.12.23, 03:40

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`
prjPath="$rootPath" # `pwd`

# Import config variables...
test -f "$scriptsPath/config.sh" && . "$scriptsPath/config.sh"
test -f "$scriptsPath/config-local.sh" && . "$scriptsPath/config-local.sh"

# NOTE: Those commands broke all the searches
#   -not \( -name '*_' -prune \) \
#   -not \( -name '*~' -prune \) \
$FINDCMD . \
  -not \( -name '.git' -prune \) \
  -not \( -name '.vscode' -prune \) \
  -not \( -name '.next' -prune \) \
  -not \( -name '.venv*' -prune \) \
  -not \( -name 'out' -prune \) \
  -not \( -name 'build*' -prune \) \
  -not \( -name '*UNUSED' -prune \) \
  -not \( -name 'publish*' -prune \) \
  -not \( -name 'node_modules' -prune \) \
  \( \
    -name '*_' \
    -o -name '*.py[co]' \
    -o -name '.*sw[op]' \
    -o -name '*.bak' \
    -o -name '*.tmp' \
    -o -name '__pycache__' \
  \) \
  -exec $RMCMD -Rvf {} \; \
; $RMCMD -Rf \
  *.log \
  .handler-saves \
  .state-save \
  local.log* \
  .*.lock \
  *_ \
  *~ \
  *.py[co] \
  .*sw[op] \
  *.bak \
  *.tmp \
; echo OK
