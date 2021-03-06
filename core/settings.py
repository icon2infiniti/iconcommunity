import os
from django.utils.translation import gettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '!w2lf5-ry3o#wcn@zyw2*e)r@pg0l=bs@rnlx63%909n#vp#8n'

DEBUG = False

ALLOWED_HOSTS = ['localhost', '157.230.7.98', 'icon.community', 'www.icon.community']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'prep',
    'dashboard',
    'news',
    'iconsensus',
    'resources',
    'developers',
    'dapps',

    'el_pagination',
    'mathfilters',
    'feedparser',
    'django_crontab',

    'ckeditor',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'iconcommunity',
        'USER': 'iconcommunityuser',
        'PASSWORD': '@icon111',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'prepsqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

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

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en', _('English')),
    ('zh-hans', _('Simplified Chinese')),
    ('ko', _('Korean')),
]

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

STATIC_ROOT = "/home/iconcommunity/staticall/"
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

#MEDIA_ROOT = "/home/iconcommunity/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


CRONJOBS = [
    ('*/15 * * * *', 'news.cron.news_cron_15m', '>> /tmp/cronjobs.log'),
    ('0 */6 * * *', 'news.cron.news_cron_6h', '>> /tmp/cronjobs.log'),
    ('0 * * * *', 'dashboard.cron.dashboard_cron_1h', '>> /tmp/cronjobs.log'),
    ('0 */6 * * *', 'dashboard.cron.dashboard_cron_6h', '>> /tmp/cronjobs.log'),
]

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'width': "100%",
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}


CORS_ORIGIN_WHITELIST = [
    "https://iconpreps.com",
    "https://icon-preps.netlify.com"
]
