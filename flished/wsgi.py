"""
WSGI config for flished project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import logging

logger = logging.getLogger(__name__)
logger.info("running wsgi.py file")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flished.settings')
logger.info("setting default settings module from wsgi.py file")
application = get_wsgi_application()
