from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403,F401

DEBUG = False

if not SECRET_KEY or SECRET_KEY == "change-me-to-a-long-random-string":
    raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set to a secure value.")

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS must be configured in production.")

CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")
if not CSRF_TRUSTED_ORIGINS:
    raise ImproperlyConfigured("DJANGO_CSRF_TRUSTED_ORIGINS must be configured in production.")

INSTALLED_APPS = [*INSTALLED_APPS, "storages"]  # noqa: F405

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SESSION_COOKIE_SECURE = env_bool("DJANGO_SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env_bool("DJANGO_CSRF_COOKIE_SECURE", default=True)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SECURE_REDIRECT_EXEMPT = [r"^health/$", r"^ready/$"]
SECURE_HSTS_SECONDS = env_int("DJANGO_SECURE_HSTS_SECONDS", default=3600)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=False,
)
SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD", default=False)
X_FRAME_OPTIONS = "DENY"

GCS_STATIC_BUCKET_NAME = env("GCS_STATIC_BUCKET_NAME", required=True)
GCS_MEDIA_BUCKET_NAME = env("GCS_MEDIA_BUCKET_NAME", required=True)
GCS_STATIC_PREFIX = env("GCS_STATIC_PREFIX", default="static").strip("/")
GCS_MEDIA_PREFIX = env("GCS_MEDIA_PREFIX", default="media").strip("/")
GCS_STATIC_CACHE_CONTROL = env(
    "GCS_STATIC_CACHE_CONTROL",
    default="public, max-age=31536000, immutable",
)
GCS_MEDIA_CACHE_CONTROL = env("GCS_MEDIA_CACHE_CONTROL", default="public, max-age=3600")


def build_gcs_url(bucket_name: str, prefix: str) -> str:
    cleaned_prefix = prefix.strip("/")
    if cleaned_prefix:
        return f"https://storage.googleapis.com/{bucket_name}/{cleaned_prefix}/"
    return f"https://storage.googleapis.com/{bucket_name}/"


STATIC_URL = env("DJANGO_STATIC_URL", default=build_gcs_url(GCS_STATIC_BUCKET_NAME, GCS_STATIC_PREFIX))
MEDIA_URL = env("DJANGO_MEDIA_URL", default=build_gcs_url(GCS_MEDIA_BUCKET_NAME, GCS_MEDIA_PREFIX))

# This deployment serves both static and media as public GCS objects.
# That keeps admin assets and public site media readable without signed URLs.
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": GCS_MEDIA_BUCKET_NAME,
            "location": GCS_MEDIA_PREFIX,
            "default_acl": None,
            "file_overwrite": False,
            "querystring_auth": False,
            "object_parameters": {
                "cache_control": GCS_MEDIA_CACHE_CONTROL,
            },
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": GCS_STATIC_BUCKET_NAME,
            "location": GCS_STATIC_PREFIX,
            "default_acl": None,
            "file_overwrite": True,
            "querystring_auth": False,
            "object_parameters": {
                "cache_control": GCS_STATIC_CACHE_CONTROL,
            },
        },
    },
}
