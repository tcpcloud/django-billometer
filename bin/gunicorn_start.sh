#!/bin/bash

NAME="billometer"
PACKAGE_NAME=$(echo "$NAME" | tr '-' '_')
DJANGODIR=/usr/lib/${NAME}
USER=billometer
GROUP=billometer
WORKERS=$(cat /proc/cpuinfo | grep -c processor)
DJANGO_SETTINGS_MODULE=${PACKAGE_NAME}.settings
DJANGO_WSGI_MODULE=${PACKAGE_NAME}.wsgi
LOG_LEVEL=debug
CHDIR="/var/lib/${NAME}"
BIND_HOST="0.0.0.0"
BIND_PORT="9753"

[ -f /etc/${NAME}/gunicorn ] && . /etc/${NAME}/gunicorn

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
. $DJANGODIR/bin/activate

export DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
cd $CHDIR
exec ${DJANGODIR}/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name ${NAME} \
  --workers ${WORKERS} \
  --user=${USER} --group=${GROUP} \
  --log-level=${LOG_LEVEL} \
  --bind=${BIND_HOST}:${BIND_PORT}
