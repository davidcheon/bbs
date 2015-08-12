"""
Django settings for bbs project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_DIRS, FILE_CHARSET,\
    DEFAULT_CHARSET, SESSION_EXPIRE_AT_BROWSER_CLOSE, SESSION_COOKIE_AGE,\
    TEMPLATE_CONTEXT_PROCESSORS
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1j^_c0e)o&gxnqbl8u^u=78f#ekgyl9sy_y3r(x&4k51b$_kin'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'django.contrib.sites',
    'debugtools',
    'south',
    'app1',
)
SITE_ID=1
MIDDLEWARE_CLASSES = (
#      'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'bbs.urls'

WSGI_APPLICATION = 'bbs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'bbs',
        'USER':'root',
        'PASSWORD':'daisongchen'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
#TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
#TEMPLATE_DIRS=(os.path.join(BASE_DIR,'templates'),)
STATICFILES_DIRS=(os.path.join(BASE_DIR,'app1/statics'),
                 )
# FILE_CHARSET='utf-8'
# DEFAULT_CHARSET='utf-8'
# LANGUAGE_CODE = 'zh-cn'
APPEND_SLASH=False
#SESSION_EXPIRE_AT_BROWSER_CLOSE=True
#SESSION_COOKIE_AGE=0
TIME_ZONE="Etc/GMT-9"
USE_TZ=False
#CACHE_BACKEND='memcached://127.0.0.1:11211/'
CACHES={
       'default':{
#                   'BACKEND':'django.core.cache.backends.memcached.PyLibMCCache',
                    'BACKEND':'django.core.cache.backends.memcached.MemcachedCache',
                  'LOCATION':['127.0.0.1:11211'],
                  }
       }
TEMPLATE_CONTEXT_PROCESSORS=(
                              'django.core.context_processors.csrf',
                             "django.contrib.auth.context_processors.auth",
                             "django.core.context_processors.request",
                             )
