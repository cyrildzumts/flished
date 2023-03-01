from django.utils.translation import ugettext_lazy as _

UNSPLASH_CREDENTIALS_KEY = "unsplash"
UNSPLASH_CACHE_KEY = f"credentials.{UNSPLASH_CREDENTIALS_KEY}"
UNSPLASH_ACCESS_KEY = "access_key"
UNSPLASH_SECRET_KEY = "secret_key"

MAX_RECENT = 5
TOP_VIEWS_MAX = 10
EMAIL_VALIDATION_DELAY = 5 #days

headers = ["", "h1","h2", "h3", "h4", "h5", "h6"]
LIST_TYPE_MAPPING = {
    'ordered': 'ol',
    'checklist': 'ul'
}

CELERY_LOGGER_HANDLER_NAME = "async"
CELERY_LOGGER_NAME = "async"
CELERY_FILE_HANDLER_CONF = {
    'level': 'INFO',
    'class': 'logging.handlers.TimedRotatingFileHandler',
    'formatter': 'file',
    'filename':'logs/flished.log',
    'when' : 'midnight'
}

"""BLOCK_MAPPING = {
        'header': render_header,
        'paragraph': render_paragraph,
        'table': render_table,
        'list': render_list,
        'linkTool': render_linkTool,
        'checklist': render_checklist,
        'quote': render_quote
}"""

ADS_FUNCTIONALITY_STORAGE = _('We require this for the core functionality of the site.')
ADS_AD_STORAGE = _('We use this cookies to show to our visitors ads that are adapted to theirs interests.')
ADS_ANALYTICS_STORAGE = _('We require this cookies to better analyse the how our visitors  use our site. This will help us to improve the usage of our site.')
ADS_PERSONALIZATION_STORAGE = _('We use this cookie to provide our visitors with the content related to their interests.')
ADS_SECURITY_STORAGE = _('We use this cookies to provide more security and authentication of the site.')

ADS_SETTINGS_LIST = [
    {'name' : _('Functionality'),'tag': 'functionality','consent_type': 'functionality_storage', 'description': ADS_FUNCTIONALITY_STORAGE, 'required': True },
    {'name' : _('Advertising'),'tag': 'advertising', 'consent_type': 'ad_storage', 'description': ADS_AD_STORAGE, 'required': True },
    {'name' : _('Analytics'),'tag': 'analytics','consent_type': 'analytics_storage', 'description': ADS_ANALYTICS_STORAGE, 'required': True },
    {'name' : _('Personalization'),'tag': 'personalization','consent_type': 'personalization_storage', 'description': ADS_PERSONALIZATION_STORAGE, 'required': False },
    {'name' : _('Security'),'tag': 'security','consent_type': 'security_storage', 'description': ADS_SECURITY_STORAGE, 'required': True },
]
