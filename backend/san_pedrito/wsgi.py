"""WSGI config for san_pedrito project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'san_pedrito.settings')

application = get_wsgi_application()