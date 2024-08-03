"""
Django settings for mymeeting project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*0ud(+ye#^9)@%9487x$c!6ciw5@@^%pe03$e6j)uyb%yoz=7u'

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
    'meetings',
    'crispy_forms',
    'crispy_bootstrap4',
    'django_summernote',
    'django_markup',
    # 'channels',
]
# settings.py
CRISPY_TEMPLATE_PACK = 'bootstrap4'
# settings.py
SUMMERNOTE_CONFIG = {
    'iframe': False,  # Use <div> instead of <iframe> for better CSS control
    'summernote': {
        'width': '100%',  # Ensure the editor takes up the full width of its container
        'height': '300px',  # Set a default height
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
    },
    'styleWithSpan': False,  # Disable <span> styling to make CSS easier to manage
}

    



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# Set the session engine (database-backed sessions by default)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Cookie settings
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 1209600  # 2 weeks, in seconds
SESSION_COOKIE_SECURE = False  # Set to True in production if using HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'  # Set to 'Strict' or 'None' as needed

# Other settings
SESSION_SAVE_EVERY_REQUEST = False  # Save the session to the database on every request
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # End session when browser is closed


ROOT_URLCONF = 'mymeeting.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mymeeting.wsgi.application'
# Add these settings if not already present

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'home'  # Change 'home' to your desired redirect URL after login
LOGOUT_URL = 'home'  # Change 'home' to your desired redirect URL after logout


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'minutes',
        'USER': 'minutes',
        'PASSWORD': '@root',
        'HOST': 'localhost',  # Set to the appropriate host if it's not localhost
        'PORT': '3306',  # Default port for MySQL
        'OPTIONS': {
            'unix_socket': '/var/run/mysqld/mysqld.sock',
        },
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

LOGIN_URL = '/accounts/login/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'