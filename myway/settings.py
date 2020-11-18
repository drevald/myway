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
    'myway'
]