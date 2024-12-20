#!/bin/sh
# @desc Check if run under .venv environment
# @changed 2024.12.21, 02:28

PYTHON=`which python`

echo "$PYTHON" | grep -q ".venv"

if [ $? = 1 ]; then
  echo "ERROR: Should run under .venv environment"
  exit 1
fi

echo "OK: Runnning under .venv environment"
