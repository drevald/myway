import os
import environ

env = environ.Env()

SECRET_KEY = 1

BASE_DIR = environ.Path(__file__) - 2

dot_env = str(BASE_DIR.path(".env"))

if os.path.exists(dot_env):
    env.read_env(dot_env)

DEBUG = True

ROOT_URLCONF = "myway.urls"

DATABASES = {
    'default': env.db(),
    'replica': env.db()
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
        'APP_DIRS': True,
        'OPTIONS': {
            "context_processors": [
                "django.template.context_processors.request",
            ]
        },        
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

ALLOWED_HOSTS = ['0.0.0.0','127.0.0.1','192.168.0.191']
