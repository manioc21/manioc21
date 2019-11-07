"""
WSGI config for moniac project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.getenv('IITA_ENV') == 'Local':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moniac.settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moniac.heroku_settings")

application = get_wsgi_application()
