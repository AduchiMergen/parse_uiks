import os
from project.settings.settings import BASE_DIR

SECRET_KEY = '29@b2yh@vl28dnmv+g(0m3*=#kl9egwc&xg(ps@2@p-i8%yp8v'

DEBUG = False

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
