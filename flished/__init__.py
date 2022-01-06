from .celery import app as celery_app
import logging

logger = logging.getLogger(__name__)
logger.info("flished __init__.py file")
__all__ = ('celery_app',)