from decouple import config
from pathlib import Path
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from django.urls import reverse_lazy
import logging
import logging.config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '1232'
DEBUG = True
# DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    # local
    'home',
    # 3rd party
    'rest_framework',
    'rest_framework.authtoken',
    'mathfilters',
    'django_crontab',
    'smart_selects',
    'widget_tweaks',
    'django_filters',
    'rest_framework_swagger',
    'drf_yasg',  # pip install drf-yasg==1.20.0
    'debug_toolbar',
    'django_extensions',
    'import_export',  # pip install django-import-export
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # new
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# debug toolbar
# INTERNAL_IPS = [
#     "127.0.0.1",
# ]

ROOT_URLCONF = 'turonun.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'turonun.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = "home.Employee"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }
]

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.StandardResultsSetPagination',
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

CRONJOBS = [
    # 6 soatda bir sms jo'natadi tug'ilgan kunlarga
    ('0 */6 * * *', 'home.bugalter.views.birthday_sms_send'),
    # 1 soatda bir sms jo'natadi
    ('* */2 * * *', 'home.bugalter.views.schedular_sms_send'),
    # 6  soatda bir sms jo'natadi
    ('* */6 * * *', 'home.views.store_product_alert_sms_send'),

]

JQUERY_URL = True
USE_DJANGO_JQUERY = True

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = (os.path.join('static'), )

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

if DEBUG is False:
    # sentry
    sentry_sdk.init(
        dsn="https://ea5cd63f0f1449908d5bfdade6d7a250@o1125038.ingest.sentry.io/6187879",
        integrations=[DjangoIntegration()],

        traces_sample_rate=1.0,

        send_default_pii=True
    )

SMS_STORE_PRODUCT_NUMBER = '+998983000796'
FIREBASE_API_KEY = "AAAAo_VpcG8:APA91bEaS70LujMQMp_ERy276XRwVxbogUN6L3_cvNclWpBaknVcZQWQ99v13T6Xtyr14BsdS0n8yrkclNnM4DHSFLxBRmarZ_OvPzqBtcNGmjXeg7XcYycXkC2xIEZ_sh1yksFc4GFJ"
SEND_NOTIFICATION_MESSAGE = 'Yangi buyurtma yaratildi!'

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': 'debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
        'django.request': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    }
})

LOGIN_URL = reverse_lazy('login')