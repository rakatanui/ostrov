#!/bin/sh
set -eu

echo "Waiting for PostgreSQL at ${POSTGRES_HOST}:${POSTGRES_PORT}..."

python - <<'PY'
import os
import sys
import time

import psycopg

settings = {
    "dbname": os.environ["POSTGRES_DB"],
    "user": os.environ["POSTGRES_USER"],
    "password": os.environ["POSTGRES_PASSWORD"],
    "host": os.environ["POSTGRES_HOST"],
    "port": os.environ["POSTGRES_PORT"],
    "connect_timeout": 3,
}

for attempt in range(1, 61):
    try:
        with psycopg.connect(**settings) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        print("PostgreSQL is available.")
        break
    except Exception as exc:
        print(f"Attempt {attempt}/60: PostgreSQL is unavailable: {exc}")
        time.sleep(1)
else:
    print("Could not connect to PostgreSQL in time.", file=sys.stderr)
    sys.exit(1)
PY

python manage.py compilemessages
python manage.py migrate --noinput

exec "$@"
