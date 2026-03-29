from .base import *  # noqa: F403,F401

DEBUG = env_bool("DJANGO_DEBUG", default=True)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

