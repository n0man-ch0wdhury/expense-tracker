"""WSGI config for budgetscope project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budgetscope.settings')

application = get_wsgi_application()