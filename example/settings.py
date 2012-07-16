import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_DIR = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'projectdb',
    }
}

TIME_ZONE = 'America/Chicago'
STATIC_URL = '/static/'
TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)
STATIC_DIR = (
    os.path.join(PROJECT_DIR, 'static'),
)
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = '-2cmgs7l$5grqwd!cyat6&6241^ah&rwn#ef5s_lm(1@0a4w&v'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'example.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'multiselect',
    'django_nose',
    'example.sample',
)

SOUTH_TESTS_MIGRATE = False

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'