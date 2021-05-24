# flake8: noqa
from foodgram.settings import *  # noqa


REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
    )
