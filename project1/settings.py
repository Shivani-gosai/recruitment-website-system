"""
Django settings for project1 project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e&&ij7@_#!s^$5uta@s7_*un29_=-%1lnx^7nfpgfx(9)&z-#*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
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

ROOT_URLCONF = 'project1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Ensure this points to your templates folder
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

WSGI_APPLICATION = 'project1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database2',
        'USER': 'root',
        'PASSWORD': 'Shivani@2005',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


import base64
from cryptography.fernet import Fernet

# Generate a key only once and save it securely
SECRET_ENCRYPTION_KEY = "5MF3M3_Fd8pyLgNNwCmRf7A3Pqp8k9WzQc8ZZwt1gwQ="

import os

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "5MF3M3_Fd8pyLgNNwCmRf7A3Pqp8k9WzQc8ZZwt1gwQ=")

# Example usage
DEBUG = os.getenv("DEBUG", "False") == "True"


LOGIN_URL = '/login/'  # Ensure this points to the correct login page
LOGIN_REDIRECT_URL = '/profile/'  # Ensure this points to the new_profile_view
LOGIN_REDIRECT_URL = "/profile/"  # Redirect to profile after login

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # This is important
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # This is important
    'django.contrib.messages.middleware.MessageMiddleware',
]


import os

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Add this line

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Store sessions in DB
SESSION_COOKIE_AGE = 86400  # Keep session for 1 day
SESSION_SAVE_EVERY_REQUEST = True  # Refresh session on every request
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Prevent session loss on browser close

# settings.py

SESSION_ENGINE = "django.contrib.sessions.backends.db"  # Stores sessions in DB
SESSION_COOKIE_AGE = 86400  # 1 day (Adjust as needed)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keeps session active even after closing browser
SESSION_COOKIE_HTTPONLY = True  # Security measure
SESSION_SAVE_EVERY_REQUEST = True  # Save session every request

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'D:\Django\project1\myapp\static']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'gosaishivani.18@gmail.com'
EMAIL_HOST_PASSWORD = '12345'  # App Password from Google (not your main password)
