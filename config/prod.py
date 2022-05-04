import os
from .settings import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False  # important

sentry_sdk.init(dsn="", integrations=[DjangoIntegration()], send_default_pii=True)


# ALLOWED_HOSTS = secrets['ALLOWED_HOST']
ALLOWED_HOSTS = ["*"]


DATABASES = secrets["DB_SETTINGS"]

WSGI_APPLICATION = "config.uwsgi.application"
