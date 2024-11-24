#!/bin/sh
# @desc Update build date/time tag file with current timestamp
# @changed 2024.11.20, 05:22
# NOTE: This script updates only .txt files not properties in `package.json`.
# Use `update-build-variables.sh` script before build.

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`
prjPath="$rootPath" # `pwd`

# Import config variables (expected variables `$DIST_REPO` and `$PUBLISH_FOLDER`)...
test -f "$scriptsPath/config.sh" && . "$scriptsPath/config.sh"
test -f "$scriptsPath/config-local.sh" && . "$scriptsPath/config-local.sh"

# Check basic required variables...
test -f "$scriptsPath/config-check.sh" && . "$scriptsPath/config-check.sh"

# node "$scriptsPath/update-build-time.js" --tz=$TIMEZONE
