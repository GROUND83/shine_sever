"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
import json
from django.core.exceptions import ImproperlyConfigured
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

secret_file = os.path.join(BASE_DIR, "secrets.json")
with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "*",
    "0.0.0.0",
    "13.209.87.72",
    "3.39.135.233",
    "*.compute.amazonaws.com",
    ".ap-northeast-2.compute.amazonaws.com",
    ".shinestudyplace.com",
]

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
PROJECT_APPS = [
    "cores.apps.CoresConfig",
    "users.apps.UsersConfig",
    "orders.apps.OrdersConfig",
    "seats.apps.SeatsConfig",
    "vertifies.apps.VertifiesConfig",
    "notices.apps.NoticesConfig",
    "alrams.apps.AlramsConfig",
    "checks.apps.ChecksConfig",
    "complaints.apps.ComplaintsConfig",
]
THIRDPARTY_APPS = ["rest_framework", "corsheaders", "storages", "sonoff"]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRDPARTY_APPS
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    # "DEFAULT_PERMISSION_CLASSES": [
    #     "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    # ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "config.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DATE_INPUT_FORMATS": ["%Y-%m-%d"],
}
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# CORS 관련 추가
# CORS_ORIGIN_WHITELIST = [
#     " https://shinestudyplace.com",
# ]
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
AUTH_USER_MODEL = "users.User"

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"


USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = []
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "uploads"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# AWS_S3_SECURE_URLS = False
# AWS_QUERYSTRING_AUTH = False

# AWS_S3_ACCESS_KEY_ID = get_secret("STORAGE_KEY")
# AWS_S3_SECRET_ACCESS_KEY = get_secret("STORAGE_SECRET")
# AWS_STORAGE_BUCKET_NAME = "shinestorage"

sentry_sdk.init(
    dsn="https://e5771c3d5bfd429db97ca19d794d02bb@o407713.ingest.sentry.io/6307964",
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
