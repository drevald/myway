DATABASE_URL = "postgres://postgres:password@127.0.0.1:5432/myway"
PORT = 8000
SECRET_KEY = 1
DEBUG = True
ROOT_URLCONF = "myway.urls"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myway',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432'
    },
}

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'myway.core'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['myway/templates'],
        # 'APP_DIRS': True,
        # 'OPTIONS': {
        #     'context_processors': [
        #         'django.template.context_processors.debug',
        #         'django.template.context_processors.request',
        #         'django.contrib.auth.context_processors.auth',
        #         'django.contrib.messages.context_processors.messages',
        #     ],
        # },
    },
]

INTERNAL_IPS = [
    '127.0.0.1',
]

STATIC_URL = "static/"