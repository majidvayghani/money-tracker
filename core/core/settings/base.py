import os
# import json
# import logstash
from pathlib import Path
from decouple import config
# from logging.handlers import RotatingFileHandler

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Ensure the logs directory exists
LOG_PATH = config('LOG_PATH', default='./log/django.log')
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)


# Security settings
SECRET_KEY = config('DJANGO_SECRET_KEY', default='your-default-secret-key')  # Use a strong secret key in production
DEBUG = config('DJANGO_DEBUG', default='False', cast=bool)

# Allowed hosts
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='').split(',')

LOCAL_APPS = [
    'transactions.apps.TransactionsConfig',
    'accounts.apps.AccountsConfig',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'health',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the custom middleware
    'core.middleware.RateLimitMiddleware',
    'core.authenticationmiddleware.CustomAuthenticationMiddleware',
]

# URL configuration
ROOT_URLCONF = 'core.urls'

# Templates configuration
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

# WSGI application
WSGI_APPLICATION = 'core.wsgi.application'

# Database settings using PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST', 'localhost'),
        'PORT': config('DATABASE_PORT', '5432'),
    }
}

# Caching with Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://localhost:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# Custom setting with user model
AUTH_USER_MODEL = "accounts.User"

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST = config('EMAIL_HOST', default='smtp.example.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='your-email@example.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='your-email-password')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@example.com')

# ELK Stack 
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'account_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'detailed',
            'filename': config('LOG_PATH')
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'account': {
            'handlers': ['account_log', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}