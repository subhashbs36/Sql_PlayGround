import os


SECRET_KEY = 'shhh'
DEBUG = True
STATIC_URL = '/static/'

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'tmp',
        'TEST': {
            'NAME': 'tmp'
        }
    },
    'alt': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'tmp2',
        'TEST': {
            'NAME': 'tmp2'
        }
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sakila',
        'USER': 'root',
        'PASSWORD': 'Jssvasa72@',
        'HOST':'localhost',
        'PORT':'3306',
    },
    'not_registered': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'tmp3',
        'TEST': {
            'NAME': 'tmp3'
        }
    }
}

EXPLORER_CONNECTIONS = {
    # 'Postgres': 'postgres',
    'MySQL1': 'mysql',
    'SQLite': 'default',
    'Another': 'alt'
}

EXPLORER_DEFAULT_CONNECTION = 'default'

ROOT_URLCONF = 'explorer.tests.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
            ],
            'debug': DEBUG
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'explorer',
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

CELERY_TASK_ALWAYS_EAGER = True

# added to help debug tasks
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Explorer-specific

EXPLORER_TRANSFORMS = (
    ('foo', '<a href="{0}">{0}</a>'),
    ('bar', 'x: {0}')
)

EXPLORER_USER_QUERY_VIEWS = {}
EXPLORER_TASKS_ENABLED = os.environ.get('ENABLE_TASKS') == 'yes'  # variable set in github action - assumed to be str
EXPLORER_S3_BUCKET = 'thisismybucket.therearemanylikeit.butthisoneismine'
