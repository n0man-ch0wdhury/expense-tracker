"""ASGI config for budgetscope project."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budgetscope.settings')

application = get_asgi_application()