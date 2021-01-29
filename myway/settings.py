import os
import environ

env = environ.Env()

BASE_DIR = environ.Path(__file__) - 2

dot_env = str(BASE_DIR.path(".env"))

if os.path.exists(dot_env):
    env.read_env(dot_env)

# DATABASE_URL = "postgres://postgres:password@127.0.0.1:5432/myway"

PORT = 8000
SECRET_KEY = 1
DEBUG = True
ROOT_URLCONF = "myway.urls"

# DATABASES = {
#     'default': env.db(),
#     'replica': env.db(), 'TEST': {'MIRROR': 'default'}
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myway',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432'
    },
    'replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mytest',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'MIRROR': 'default',
        }
    }
}

INSTALLED_APPS = [
    'myway.core',
    'django.contrib.sessions',
    'crispy_forms',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['myway/templates'],
        'OPTIONS': {
            "context_processors": [
                "django.template.context_processors.request",
            ]
        },        
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

ALLOWED_HOSTS = ['0.0.0.0','127.0.0.1','192.168.0.191']