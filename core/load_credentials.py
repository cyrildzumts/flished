from django.core.cache import cache
from core import constants
from flished import settings
import json

import logging

CACHE = cache
logger = logging.getLogger(__name__)

def load_unsplash_credentials():
    credential = CACHE.get(constants.UNSPLASH_CACHE_KEY)
    if credential:
         return credential
    try:
        with open(settings.CREDENTIALS_FILE, 'r') as config:
            data = json.loads(config.read())
            if constants.UNSPLASH_CREDENTIALS_KEY in data:
                credential = data.get(constants.UNSPLASH_CREDENTIALS_KEY)
                CACHE.set(constants.UNSPLASH_CACHE_KEY, credential)
                return credential
            
    except Exception as e:
        logger.warn(f"Error loading config file {settings.CREDENTIALS_FILE}")
        logger.exception(e)
    return {"error": "no credentials"}