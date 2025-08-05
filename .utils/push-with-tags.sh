#!/bin/sh
# @desc Create/update version tag (from build folder)
# @changed 2024.12.30, 15:44

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`

# Import config variables...
test -f "$scriptsPath/config.sh" && . "$scriptsPath/config.sh"
test -f "$scriptsPath/config-local.sh" && . "$scriptsPath/config-local.sh"

# Check basic required variables...
test -f "$rootPath/config-check.sh" && . "$rootPath/config-check.sh" --omit-publish-folder-check

VERSION_FILE="$rootPath/project-version.txt"
VERSION=`cat $VERSION_FILE`
TIMESTAMP=`date -r $VERSION_FILE "+%Y.%m.%d %H:%M:%S %z"`
TIMETAG=`date -r $VERSION_FILE "+%y%m%d-%H%M"`
PROJECT_INFO="v.$VERSION / $TIMESTAMP"

echo "Publishing source code $PROJECT_INFO..."

TAG_VALUE="v.$VERSION"
echo "Create/update tag $TAG_VALUE..." \
  && git tag -f "$TAG_VALUE" \
  && git push origin -f --tags \
  && git pull origin \
  && echo "OK"
