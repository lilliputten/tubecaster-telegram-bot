#!/bin/sh
# @desc Initialize prisma environment (under venv)
# @changed 2024.12.19, 23:11

echo "Initializing prisma environment (under venv)..." && \
  prisma generate && \
  prisma db push && \
  DATABASE_URL='file:.data-test.db' prisma db push && \
  echo "OK"
