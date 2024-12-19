#!/bin/sh
# @desc Run python tests
# @changed 2024.12.20, 00:49

echo "Run python tests..." && \
  python -m unittest discover -v -f -t . -s . -p *_test.py && \
  echo OK
