import os
import sys
from datetime import timedelta
from pathlib import Path

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

SECRET_KEY = config['DJANGO_APP_SECRET_KEY']

DEBUG = int(config['DJANGO_APP_DEBUG'])

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
ASGI_APPLICATION = 'unicat.asgi.application'

DATABASES = {
    'default': {},
    'master': {
        'ENGINE': config['DJANGO_APP_DATABASE_SQL_ENGINE'],
        'NAME': config['DJANGO_APP_DATABASE_SQL_MASTER_DATABASE'],
        'USER': config['DJANGO_APP_DATABASE_SQL_MASTER_USER'],
        'PASSWORD': config['DJANGO_APP_DATABASE_SQL_MASTER_PASSWORD'],
        'HOST': config['DJANGO_APP_DATABASE_SQL_MASTER_HOST'],
        'PORT': config['DJANGO_APP_DATABASE_SQL_MASTER_PORT'],
        'TEST': {
            'DEPENDENCIES': [],
        },
    },
    'slave': {
        'ENGINE': config['DJANGO_APP_DATABASE_SQL_ENGINE'],
        'NAME': config['DJANGO_APP_DATABASE_SQL_REPLICA_DATABASE'],
        'USER': config['DJANGO_APP_DATABASE_SQL_REPLICA_USER'],
        'PASSWORD': config['DJANGO_APP_DATABASE_SQL_REPLICA_PASSWORD'],
        'HOST': config['DJANGO_APP_DATABASE_SQL_REPLICA_HOST'],
        'PORT': config['DJANGO_APP_DATABASE_SQL_REPLICA_PORT'],
    },
}

DATABASE_ROUTERS = [config['DJANGO_APP_DATABASE_ROUTER']]

CACHES = {
    'default': {
        'BACKEND': config['DJANGO_APP_CACHES_BACKEND'],
        'LOCATION': config['DJANGO_APP_CACHES_LOCATION'],
        'TIMEOUT': 3600,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
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
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

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
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.'
                                'default_user_authentication_rule',

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
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'access-control-allow-credentials',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

SUMMERNOTE_CONFIG = {
    'attachment_absolute_uri': True,
}

GRAPHENE = {
    'SCHEMA': 'unicat.graphql.schema.schema',
    'MIDDLEWARE': [
        'unicat.middleware.loader_middleware.LoaderMiddleware',
    ]
}

if DEBUG:
    GRAPHENE['MIDDLEWARE'] += ['graphene_django.debug.DjangoDebugMiddleware', ]

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
