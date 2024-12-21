#!/bin/sh
# @desc Create venv for user www-data
# @changed 2024.12.21, 08:15

echo "Creating venv for www-data..." \
&& sudo -u www-data python -m virtualenv /var/www/.venv-default \
&& sudo -u www-data chmod -Rf a+rw /var/www/.venv-default \
&& sudo -u www-data /var/www/.venv-default/bin/pip install -r requirements.txt \
&& sudo -u www-data /var/www/.venv-default/bin/python -m prisma format \
&& echo OK

# This command cause an error ('Error: Generator "prisma-client-py" failed: /bin/sh: 1: prisma-client-py: not found'):
# sudo -u www-data /var/www/.venv-default/bin/python -m prisma db push --accept-data-loss
# See also:
# sudo -u www-data sh
