FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app/src \
    DJANGO_SETTINGS_MODULE=config.settings.production \
    PORT=8080

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y gettext \
    && rm -rf /var/lib/apt/lists/*

COPY requirements /app/requirements

RUN pip install --upgrade pip \
    && pip install -r /app/requirements/production.txt

COPY . /app

WORKDIR /app/src
RUN DJANGO_SETTINGS_MODULE=config.settings.base \
    DJANGO_SECRET_KEY=build-time-secret \
    django-admin compilemessages

RUN addgroup --system app \
    && adduser --system --ingroup app --home /home/app app \
    && chmod +x /app/docker/web/entrypoint.sh /app/docker/web/start-web.sh \
    && chown -R app:app /app

WORKDIR /app/src
USER app

CMD ["/app/docker/web/start-web.sh"]
