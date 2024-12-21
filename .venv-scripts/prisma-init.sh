#!/bin/sh
# @desc Initialize prisma environment (under venv)
# @changed 2024.12.19, 23:11

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`

test -f "$scriptsPath/check-venv.sh" && . "$scriptsPath/check-venv.sh"

echo "Initializing prisma environment (under venv)..." \
&& prisma format \
&& prisma generate \
&& prisma db push \
&& DATABASE_URL='file:.data-test.db' prisma db push \
&& echo "OK"
