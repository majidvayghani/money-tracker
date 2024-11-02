from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='your-gmail-address@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='your-gmail-password')