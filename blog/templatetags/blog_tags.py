from django import template
from django.utils.translation import gettext_lazy as _
from blog import constants as Constants
from flished import utils
import logging

logger = logging.getLogger(__name__)
register = template.Library()

@register.filter
def post_status_value(key):
    k,v = utils.find_element_by_key_in_tuples(key, Constants.POST_STATUS)
    if v is None:
        logger.info(f"post_status_value : Could not found value  for key \"{key}\"")
        return key
    return v