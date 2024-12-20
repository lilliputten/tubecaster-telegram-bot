#!/bin/sh
# @desc Check if run under .venv environment
# @changed 2024.12.20, 12:57

PYTHON=`which python`

if [[ $PYTHON != *".venv"* ]]; then
   echo "Should run under .venv environment"
   exit 1
fi

echo "Ok, runnning under .venv environment"
