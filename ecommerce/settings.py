"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from decouple import config

import os
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

#SECRET_KEY = config('SECRET_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY', default='django-insecure-x%4(_&yn5q7807iq@c0e6+h9)k%=sa$k8prna-job5^k(m1!6o')
#SECRET_KEY = 'django-insecure-x%4(_&yn5q7807iq@c0e6+h9)k%=sa$k8prna-job5^k(m1!6o'

# SECURITY WARNING: don't run with debug turned on in production!

#DEBUG = config('DEBUG', cast=bool)
DEBUG = 'RENDER' not in os.environ
DEBUG_PROPAGATE_EXCEPTIONS = True

#ALLOWED_HOSTS = ['ecommerce-env.eba-pr8br5qc.us-west-2.elasticbeanstalk.com']
ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'category',
    'accounts',
    'store',
    'carts',
    'orders',
    'admin_honeypot',
    'whitenoise.runserver_nostatic',
    'storages',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_session_timeout.middleware.SessionTimeoutMiddleware",

    'whitenoise.middleware.WhiteNoiseMiddleware',
]

SESSION_EXPIRE_SECONDS = 3600
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = 'accounts/login'

ROOT_URLCONF = "ecommerce.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'category.context_processors.menu_links',
                'carts.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = "ecommerce.wsgi.application"
AUTH_USER_MODEL = 'accounts.Account'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

#DATABASES = {
    #"default": {
        #"ENGINE": "django.db.backends.sqlite3",
        #"NAME": BASE_DIR / "db.sqlite3",
    #}
#}

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:postgres@localhost:5432/mysite',
        conn_max_age=600
    )
}




# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

#STATIC_URL = '/static/'
#STATIC_ROOT = BASE_DIR /'static'
#STATICFILES_DIRS = [
#    'ecommerce/static'
#]
#STATIC_URL = '/static/'
# Following settings only make sense on production and may break development environments.
if not DEBUG:    # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    #STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    #STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage
    AWS_ACCESS_KEY_ID= config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY=config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME=config('AWS_STORAGE_BUCKET_NAME')

    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_DEFAULT_ACL = 'public-read'

    STATIC_LOCATION= 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'ecommerce.storage_backends.MediaStore'

    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'ecommerce/static'),)
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')


#MEDIA_URL = '/media/'
#MEDIA_ROOT = BASE_DIR /'media'

#MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR : 'danger',
}

#ANYMAIL = { "SENDGRID_API_KEY": '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', }
#EMAIL_DEFAULT = "ecommercejajic@gmail.com"
#EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT',cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
#Default primary key field type
#https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
