# flake8: noqa
from foodgram.settings import *  # noqa

LOGGING = None
SECRET_KEY = 'daf45edee8821f921abc11cbb69058e12d60e9ba69851881fb'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}