import os
import sys
from datetime import timedelta
from pathlib import Path

import stripe
from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent

config = {
    **dotenv_values('.env'),
    **dotenv_values('.env.local'),
    **dotenv_values('.env.development.local'),
    **dotenv_values('.env.production.local'),
    **os.environ,
}

if 'test' in sys.argv:
    config = {
        **dotenv_values('.env.test.local')
    }
    stripe.api_base = config.get('DJANGO_APP_STRIPE_LOCAL_API')
    CELERY_TASK_ALWAYS_EAGER = True

TEST_RUNNER = 'snapshottest.django.TestRunner'

stripe.api_key = config.get('DJANGO_APP_STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = config.get('DJANGO_APP_STRIPE_WEBHOOK_SECRET')

SECRET_KEY = config.get('DJANGO_APP_SECRET_KEY')

DEBUG = int(config.get('DJANGO_APP_DEBUG'))

CELERY_TASK_ALWAYS_EAGER = DEBUG

MAIN_HOST = config.get('DJANGO_APP_MAIN_HOST')
ALLOWED_HOSTS = config.get('DJANGO_APP_ALLOWED_HOSTS').split(' ')

AUTH_USER_MODEL = 'users.User'

PASSWORD_HASHERS = config.get('DJANGO_APP_PASSWORD_HASHERS').split(' ')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'aldjemy',
    'corsheaders',
    'django_celery_results',
    'django_filters',
    'django_prometheus',
    'django_summernote',
    'drf_yasg',
    'graphene_django',
    'import_export',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    'courses',
    'comments',
    'events',
    'feedbacks',
    'lessons',
    'resources',
    'payments',
    'users',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'users.middleware.CookiesMiddleware.CookiesMiddleware',

    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'unicat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'unicat.wsgi.application'

DATABASES = {
    'default': {},
    'master': {
        'ENGINE': config.get('DJANGO_APP_DATABASE_SQL_ENGINE'),
        'NAME': config.get('DJANGO_APP_DATABASE_SQL_MASTER_DATABASE'),
        'USER': config.get('DJANGO_APP_DATABASE_SQL_MASTER_USER'),
        'PASSWORD': config.get('DJANGO_APP_DATABASE_SQL_MASTER_PASSWORD'),
        'HOST': config.get('DJANGO_APP_DATABASE_SQL_MASTER_HOST'),
        'PORT': config.get('DJANGO_APP_DATABASE_SQL_MASTER_PORT'),
        'TEST': {
            'DEPENDENCIES': [],
        },
        'ATOMIC_REQUESTS': True,
    },
    'slave': {
        'ENGINE': config.get('DJANGO_APP_DATABASE_SQL_ENGINE'),
        'NAME': config.get('DJANGO_APP_DATABASE_SQL_REPLICA_DATABASE'),
        'USER': config.get('DJANGO_APP_DATABASE_SQL_REPLICA_USER'),
        'PASSWORD': config.get('DJANGO_APP_DATABASE_SQL_REPLICA_PASSWORD'),
        'HOST': config.get('DJANGO_APP_DATABASE_SQL_REPLICA_HOST'),
        'PORT': config.get('DJANGO_APP_DATABASE_SQL_REPLICA_PORT'),
    },
}

DATABASE_ROUTERS = (config.get('DJANGO_APP_DATABASE_ROUTER'),)

CACHES = {
    'default': {
        'BACKEND': config.get('DJANGO_APP_CACHES_BACKEND'),
        'LOCATION': config.get('DJANGO_APP_CACHES_LOCATION'),
        'TIMEOUT': 3600,
    }
}

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = config.get('CELERY_BROKER_URL')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.NumericPasswordValidator'
        ),
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': (
        'unicat.rest.pagination.DynamicPagination.DynamicPagination'
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}

CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = config.get('DJANGO_APP_CSRF_TRUSTED_ORIGINS').split(' ')
CORS_ALLOWED_ORIGINS = config.get('DJANGO_APP_CORS_ALLOWED_ORIGINS').split(' ')

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'access-control-allow-credentials',
    'access-control-expose-headers',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'stripe-signature',
]

SUMMERNOTE_CONFIG = {
    'attachment_absolute_uri': True,
}

GRAPHENE = {
    'SCHEMA': 'unicat.graphql.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
        'unicat.middleware.LoaderMiddleware.LoaderMiddleware',
    ],
    'TESTING_ENDPOINT': '/graphql/',
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'graphql_jwt.backends.JSONWebTokenBackend',
]

GRAPHQL_JWT = {
    'JWT_ALLOW_ANY_HANDLER': 'unicat.graphql.functions.allow_any',
    'JWT_ALGORITHM': SIMPLE_JWT.get('ALGORITHM'),
    'JWT_AUTH_HEADER_PREFIX': SIMPLE_JWT.get('AUTH_HEADER_TYPES')[0],
    'JWT_AUTH_HEADER_NAME': SIMPLE_JWT.get('AUTH_HEADER_NAME'),
    'JWT_SECRET_KEY': SIMPLE_JWT.get('SIGNING_KEY'),
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=365),
    'JWT_DECODE_HANDLER': 'unicat.graphql.functions.jwt_decode',
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': (
        'unicat.graphql.functions.get_username_by_payload'
    ),
    'JWT_GET_USER_BY_NATURAL_KEY_HANDLER': (
        'unicat.graphql.functions.get_user_by_natural_key'
    ),
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config.get('DJANGO_APP_EMAIL_HOST')
EMAIL_PORT = config.get('DJANGO_APP_EMAIL_PORT')
EMAIL_HOST_USER = config.get('DJANGO_APP_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config.get('DJANGO_APP_EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = int(config.get('DJANGO_APP_EMAIL_USE_TLS', 0))
EMAIL_USE_SSL = int(config.get('DJANGO_APP_EMAIL_USE_SSL', 0))

if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'sql.log',
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }
