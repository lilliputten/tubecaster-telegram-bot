#!/bin/sh
# @desc Increment version number
# @changed 2024.12.02, 02:34

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`

# Import config variables...
test -f "$scriptsPath/config.sh" && . "$scriptsPath/config.sh"
test -f "$scriptsPath/config-local.sh" && . "$scriptsPath/config-local.sh"

# Check basic required variables...
test -f "$rootPath/config-check.sh" && . "$rootPath/config-check.sh" --omit-publish-folder-check

# Read version from file...
VERSION_FILE="$rootPath/VERSION"
BACKUP="$VERSION_FILE.bak"

# PATCH_NUMBER=`cat "$VERSION_FILE"`

NEXT_PATCH_NUMBER="0"

# test -f "$VERSION_FILE" || echo "0.0.0" > "$VERSION_FILE"
if [ ! -f "$VERSION_FILE" ]; then
  echo "NO PREVIOUS VERSION INFO!"
  echo "0.0.0" > "$VERSION_FILE"
else
  PATCH_NUMBER=`cat "$VERSION_FILE" | sed "s/^\(.*\)\.\([0-9]\+\)$/\2/"`
  # Increment patch number
  NEXT_PATCH_NUMBER=`expr $PATCH_NUMBER + 1`
fi

cp "$VERSION_FILE" "$BACKUP" \
  && cat "$BACKUP" \
    | sed "s/^\(.*\)\.\([0-9]\+\)$/\1.$NEXT_PATCH_NUMBER/" \
    > "$VERSION_FILE" \
  && rm "$BACKUP" \
  && echo "Updated version: `cat $VERSION_FILE`" \
  && sh "$scriptsPath/update-build-variables.sh" \
  && VERSION=`cat "$VERSION_FILE"` \
  && echo "Done"
