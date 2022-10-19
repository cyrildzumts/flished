from flished import settings
from django.contrib.auth.models import User
from blog import blog_service
from core.resources import ui_strings as UI_STRINGS
import logging

logger = logging.getLogger(__name__)

def site_context(request):
    is_dashboard_allowed = False
    if request.user.is_authenticated:
        is_dashboard_allowed = request.user.has_perm('dashboard.can_view_dashboard')

    context = {
        'site_name' : settings.SITE_NAME,
        'SITE_NAME' : settings.SITE_NAME,
        'SITE_HOST' : settings.SITE_HOST,
        'CONTACT_MAIL': settings.CONTACT_MAIL,
        'SITE_HEADER_BG': settings.SITE_HEADER_BG,
        'META_KEYWORDS': UI_STRINGS.HOME_META_KEYWORDS,
        'META_DESCRIPTION': UI_STRINGS.HOME_META_DESCRIPTION,
        'categories': blog_service.get_categories(),
        'redirect_to' : '/',
        'is_dashboard_allowed' : is_dashboard_allowed,
        'dev_mode' : settings.DEBUG,
        'ALLOW_GOOGLE_ANALYTICS' : settings.ALLOW_GOOGLE_ANALYTICS,
        'next_url' : request.path,
        'CSP_NONCE': request.META.get('CSP_NONCE', ''),
    }
    return context