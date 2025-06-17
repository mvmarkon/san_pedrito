"""ASGI config for san_pedrito project."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'san_pedrito.settings')

application = get_asgi_application()