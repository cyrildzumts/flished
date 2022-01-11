from celery import shared_task
#from logging.handlers import TimedRotatingFileHandler
from core.constants import CELERY_LOGGER_NAME
import logging

async_logger = logging.getLogger(CELERY_LOGGER_NAME)
#async_logger.addHandler(TimedRotatingFileHandler(**CELERY_FILE_HANDLER_CONF))

@shared_task
def async_logger_task(message, level):
    async_logger.log(level=level, msg=message)