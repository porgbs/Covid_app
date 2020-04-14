from .base import *
DEBUG = False


X_FRAME_OPTIONS = 'ALLOW-FROM *'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'http://localhost:4200',
)