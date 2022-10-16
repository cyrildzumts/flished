from pathlib import Path
from django.utils.translation import ugettext_lazy as _
import django.dispatch
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY          =  os.environ['FLISHED_SECRET_KEY']
SITE_NAME           =  os.environ.get('FLISHED_SITE_NAME', 'FLISHED')
CELERY_BROKER_URL   = os.environ.get('FLISHED_CELERY_BROKER_URL')
CELERY_BACKEND      = os.environ.get('FLISHED_CELERY_BACKEND')

CREDENTIALS_FILE = os.environ.get('FLISHED_CREDENTIALS_FILE', "credentials.json")

CELERY_DEFAULT_QUEUE = "flished-default"
CELERY_DEFAULT_EXCHANGE = "flished-default"
CELERY_DEFAULT_ROUTING_KEY = "flished-default"

CELERY_LOGGER_HANDLER_NAME = "async"
CELERY_LOGGER_NAME = "async"
CELERY_LOGGER_QUEUE = "flished-logger"
CELERY_LOGGER_EXCHANGE = "flished-logger"
CELERY_LOGGER_ROUTING_KEY = "flished-logger"

CELERY_OUTGOING_MAIL_QUEUE = "flished-outgoing-mails"
CELERY_OUTGOING_MAIL_EXCHANGE = "flished-mail"
CELERY_OUTGOING_MAIL_ROUTING_KEY = "flished.mail.outgoing"


CELERY_IDENTIFICATION_QUEUE = "flished-ident"
CELERY_IDENTIFICATION_EXCHANGE = "flished-ident"
CELERY_IDENTIFICATION_ROUTING_KEY = "flished.identification"
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'

CELERY_NAMESPACE = 'CELERY'
CELERY_APP_NAME = 'flished'
#EMAIL SETTINGS
EMAIL_HOST = os.environ.get('FLISHED_EMAIL_HOST')
EMAIL_PORT = os.environ.get('FLISHED_EMAIL_PORT')
EMAIL_HOST_PASSWORD = os.environ.get('FLISHED_EMAIL_PASSWORD')
EMAIL_HOST_USER = os.environ.get('FLISHED_EMAIL_USER')
DEFAULT_FROM_EMAIL = os.environ.get('FLISHED_DEFAULT_FROM_EMAIL', 'FLISHED <info@flished.com>')
CONTACT_MAIL =  os.environ.get('FLISHED_CONTACT_MAIL')
ADMIN_EXTERNAL_EMAIL = os.environ.get("FLISHED_ADMIN_EXTERNAL_EMAIL")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_BACKEND = os.environ.get('FLISHED_EMAIL_BACKEND')
DJANGO_EMAIL_TEMPLATE = "tags/template_email_new.html"
DJANGO_EMAIL_TO_ADMIN_TEMPLATE = "tags/admin_newuser_template_email.html"
DJANGO_EMAIL_TEMPLATE_TXT = "tags/template_email.txt"
DJANGO_WELCOME_EMAIL_TEMPLATE = "welcome_email_new.html"
DJANGO_VALIDATION_EMAIL_TEMPLATE = "validation_email_new.html"
DJANGO_PUBLISHED_CONFIRMATION_EMAIL_TEMPLATE = "tags/published_confirmation_email_new.html"

SEND_USER_LOGGED_IN_SIGNAL = True
SEND_USER_REGISTERED_SIGNAL = True
SIGNA_USER_LOGGED_IN = django.dispatch.Signal()
SIGNA_USER_REGISTERED = django.dispatch.Signal()

ALLOWED_HOSTS = [os.getenv('FLISHED_ALLOWED_HOST')]
SITE_HOST = os.getenv('FLISHED_HOST')


ALLOW_GOOGLE_ANALYTICS = os.environ.get('ALLOW_GOOGLE_ANALYTICS', 'true') == 'true'
#CSRF_COOKIE_SECURE = not DEV_MODE

SITE_HEADER_BG = "#eadbcb"

TEST_USER_PREFIX = "testuser_"

JSON_LD_CONTEXT = "https://schema.org/"
JSON_LD_TYPE_WEBSITE = "WebSite"
JSON_LD_TYPE_PRODUCT = "Product"
JSON_LD_TYPE_OFFER = "Offer"
JSON_LD_TYPE_SEARCHACTION = "SearchAction"
JSON_LD_TYPE_ENTRY_POINT = "EntryPoint"
JSON_LD_AGGREGATE_OFFER = "AggregateOffer"
JSON_LD_TYPE_OFFERS = "Offers"
JSON_LD_PRODUCT_LIST = "ItemList"
JSON_LD_PRODUCT_LIST_ELEMENT = "itemListElement"
JSON_LS_PRODUCT_IN_STOCK = "https://schema.org/InStock"
JSON_LS_PRODUCT_OUT_OF_STOCK_STOCK = "https://schema.org/OutOfStock"
JSON_LD_TYPE_COLLECTIONPAGE = "CollectionPage"
JSON_LD_TYPE_WEBPAGE = "WebPage"
JSON_LD_TYPE_BREADCRUMBLIST = "BreadcrumbList"
JSON_LD_TYPE_LISTITEM = "ListItem"
JSON_LD_PRODUCT_NEW_CONDITION = "NewCondition"

#CSP SETTING
CSP_DEFAULT_SRC = ["'self'", "*.googleadservices.com", "*.google.de", "*.google.com", "*.google.fr", "*.g.doubleclick.net", "*.googlesyndication.com"]
CSP_SCRIPT_SRC = ["'self'", "*.googleadservices.com", "*.google.de", "*.google.com", "*.google.fr", "*.g.doubleclick.net", "*.googlesyndication.com",
"*.lyshoping.com", "*.flished.com", "*.lipa-betaal.com", "*.googletagmanager.com", "*.google-analytics.com", "*.bootstrapcdn.com", "*.fontawesome.com"]
CSP_CONNECT_SRC = ["'self'", "*.googleadservices.com", "*.google.de", "*.google.com", "*.google.fr", "*.g.doubleclick.net", "*.googlesyndication.com",
"*.lyshoping.com", "*.flished.com", "*.lipa-betaal.com", "*.googletagmanager.com", "*.google-analytics.com"]
CSP_IMG_SRC = ["'self'", "*.googleadservices.com", "*.google.de", "*.google.com", "*.google.fr", "*.g.doubleclick.net", "*.googlesyndication.com",
"*.lyshoping.com", "*.flished.com", "*.lipa-betaal.com", "*.googletagmanager.com", "*.google-analytics.com", "*.bootstrapcdn.com", "*.fontawesome.com",
 "https://twemoji.maxcdn.com", "https://images.unsplash.com", "*.gstatic.com"]
CSP_STYLE_SRC = ["*.flished.com", "*.fontawesome.com", "*.bootstrapcdn.com", "*.googleapis.com", "https://www.googletagmanager.com", "*.googleadservices.com", "*.google.de", "*.google.com", "*.google.fr", "*.g.doubleclick.net", "*.googlesyndication.com"]
CSP_FONT_SRC = ["'self'", "*.googleadservices.com", "*.google.de", "*.google.com", "*.google.fr", "*.g.doubleclick.net", "*.googlesyndication.com",
 "*.flished.com", "*.googletagmanager.com", "*.google-analytics.com", "*.bootstrapcdn.com", "*.fontawesome.com", "*.gstatic.com"]
CSP_FRAME_ANCESTORS = ["'self'", "*.googleadservices.com", "*.google.de", "*.google.com", "*.google.fr", "*.g.doubleclick.net", "*.googlesyndication.com",
"*.lyshoping.com", "*.flished.com", "*.lipa-betaal.com", "*.googletagmanager.com", "*.google-analytics.com"]
CSP_INCLUDE_NONCE_IN = ['script-src']

# RESTFRAMEWORK SETTINGS
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'accounts',
    'api.apps.ApiConfig',
    'blog.apps.BlogConfig',
    'core.apps.CoreConfig',
    'dashboard.apps.DashboardConfig',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'flished.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.core_context',
                'flished.context_processors.site_context',
                'csp.context_processors.nonce',
            ],
        },
    },
]

WSGI_APPLICATION = 'flished.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'dev': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, f"{SITE_NAME}.db"),
    },
    'production': {
	'ENGINE':  os.environ.get('FLISHED_DATABASE_ENGINE'),
	'NAME'	:  os.environ.get('FLISHED_DATABASE_NAME'),
	'USER'	:  os.environ.get('FLISHED_DATABASE_USERNAME'),
	'PASSWORD':  os.environ.get('FLISHED_DATABASE_PW'),
	'HOST'	:  os.environ.get('FLISHED_DATABASE_HOST') ,
	'PORT' 	:  os.environ.get('FLISHED_DATABASE_PORT'),
    'OPTIONS' : {
        'sslmode': 'require'
    },
    'TEST'  :{
        'NAME': os.getenv('FLISHED_TEST_DATABASE', 'test_db'),
    },
   },

}
DEFAULT_DATABASE = os.environ.get('DJANGO_DATABASE', 'dev')
DATABASES['default'] = DATABASES[DEFAULT_DATABASE]
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get(f"{SITE_NAME}_DEBUG",'false') == 'true'
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'file': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'async': {
            'format': '{message}',
            'style': '{',
        },
    },

    'handlers': {
        'async':{
            'level': 'INFO',
            'class': 'core.logging.handlers.AsyncLoggingHandler',
            'formatter': 'async',
            'queue': CELERY_LOGGER_QUEUE,
            'routing_key': CELERY_LOGGER_ROUTING_KEY,
            'exchange': CELERY_LOGGER_EXCHANGE
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'file',
            'filename':'logs/flished.log',
            'when' : 'midnight'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '' : {
            'level': 'DEBUG',
            'handlers': ['console', 'async'],
            'propagate': False,
        },
        'async':{
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': False
        },
        'django': {
            'level': 'WARNING',
            'handlers': ['async'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'async'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['console', 'async'],
            'level': 'WARNING',
            'propagate': True,
        },
        'PIL':{
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        }
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fr'
LANGUAGES = (
    ('fr',_('French')),
    ('en',_('English')),
)
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
