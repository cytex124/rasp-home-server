from .base import *
from corsheaders.defaults import default_headers
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

# TODO: Change in the future
ALLOWED_HOSTS = ['*']
# TODO: Change in the future
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = default_headers + (
    'Access-Control-Allow-Origin',
)

# TODO: Change in the future
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static_dir"),)

# TODO: Change in the future
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
MEDIAFILES_DIRS = (os.path.join(BASE_DIR, "media_dir"),)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['HS_PSQL_DBNAME'],
        'USER': os.environ['HS_PSQL_USER'],
        'PASSWORD': os.environ['HS_PSQL_PW'],
        'HOST': os.environ['HS_PSQL_HOST'],
        'PORT': os.environ['HS_PSQL_PORT'],
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}/1".format(os.environ['REDIS_URL_WITH_PORT']),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": os.environ['HS_CACHE_KEY_PREFIX']
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ['HS_EMAIL_HOST']
EMAIL_PORT = os.environ['HS_EMAIL_PORT']
EMAIL_HOST_USER = os.environ['HS_EMAIL_USER']
EMAIL_HOST_PASSWORD = os.environ['HS_EMAIL_PW']

sentry_sdk.init(
    dsn=os.environ['SENTRY_URL'],
    integrations=[DjangoIntegration()]
)