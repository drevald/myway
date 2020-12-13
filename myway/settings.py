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
    'django.contrib.sessions'
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