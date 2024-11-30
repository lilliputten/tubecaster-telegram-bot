#!/bin/sh
# vim: ft=sh
# @desc Config variables (common version -- stored in repository)
# @changed 2024.12.01, 02:46

IS_WINDOWS=`echo "${OS}" | grep -i windows`
IS_CYGWIN=`uname | grep -i "CYGWIN"`

PYTHON_RUNTIME="python"

# # Set specific python executable path (may be overrided in `config-local.sh`, see `config-local.sh.TEMPLATE`)...
# PYTHON_RUNTIME="/usr/bin/python3.9"
# if [ "$IS_WINDOWS" ]; then
#   PYTHON_RUNTIME="C:/Python39/python.exe"
# fi

SRC_TAG_PREFIX="v" # "v" for default "v.X.Y.Z"

# TODO: To use generic `init-crossplatform-command-names.sh`?
FINDCMD="find"
SORTCMD="sort"
GREPCMD="grep"
RMCMD="rm"
# # Override posix commands for cygwin or/and windows (may be overrided in `config-local.sh`, see `config-local.sh.TEMPLATE`)...
if [ "$IS_CYGWIN" ]; then
    # Don't use windows' own native commands
    FINDCMD="find_"
    SORTCMD="sort_"
    GREPCMD="grep_"
fi

# Timezone for timestamps (GMT, Europe/Moscow, Asia/Bangkok, Asia/Tashkent, etc)
TIMEZONE="Europe/Moscow"

PROJECT_INFO_FILE="static/project-info.txt"

