"""
Django settings for expense_tracker project.
CSC 226 - Web Database Applications (Fall 2026).
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured
from django.core.management.utils import get_random_secret_key

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get('DEBUG', 'True').strip().lower() in ('1', 'true', 'yes')

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = get_random_secret_key()
    else:
        raise ImproperlyConfigured('SECRET_KEY must be set when DEBUG is False')

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost,.pythonanywhere.com').split(',')
    if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.pythonanywhere.com',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracker',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'expense_tracker.urls'

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

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

WSGI_APPLICATION = 'expense_tracker.wsgi.application'

SUPPORTED_ENGINES = {
    'django.db.backends.mysql': {
        'NAME': os.environ.get('DB_NAME', 'expense_tracker'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    },
    'django.db.backends.sqlite3': {
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

_raw_engine = os.environ.get('DB_ENGINE', 'sqlite').strip().lower()
if _raw_engine in ('mysql', 'django.db.backends.mysql'):
    DB_ENGINE = 'django.db.backends.mysql'
elif _raw_engine in ('sqlite', 'sqlite3', 'django.db.backends.sqlite3'):
    DB_ENGINE = 'django.db.backends.sqlite3'
else:
    DB_ENGINE = os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3')

if DB_ENGINE not in SUPPORTED_ENGINES:
    raise ImproperlyConfigured(
        f"Unsupported DB_ENGINE '{os.environ.get('DB_ENGINE')}'. Must be one of: ['sqlite', 'mysql', 'django.db.backends.sqlite3', 'django.db.backends.mysql']"
    )

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        **SUPPORTED_ENGINES[DB_ENGINE],
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
