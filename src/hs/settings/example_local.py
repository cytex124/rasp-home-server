'''
USE THIS ONLY LOCALLY.
'''

from .base import *
from corsheaders.defaults import default_headers

# Example Key
SECRET_KEY = ''

DEBUG = True

ALLOWED_HOSTS = [
    '*'
]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = default_headers + (
    'Access-Control-Allow-Origin',
)

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static_dir"),)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
MEDIAFILES_DIRS = (os.path.join(BASE_DIR, "media_dir"),)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": ""
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''