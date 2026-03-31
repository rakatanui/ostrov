#!/bin/sh
set -eu

exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT:-8080}" \
  --workers "${GUNICORN_WORKERS:-2}" \
  --threads "${GUNICORN_THREADS:-4}" \
  --timeout "${GUNICORN_TIMEOUT:-120}" \
  --graceful-timeout "${GUNICORN_GRACEFUL_TIMEOUT:-30}" \
  --keep-alive "${GUNICORN_KEEPALIVE:-5}" \
  --worker-tmp-dir /dev/shm \
  --access-logfile - \
  --error-logfile - \
  --log-level "${GUNICORN_LOG_LEVEL:-info}"
