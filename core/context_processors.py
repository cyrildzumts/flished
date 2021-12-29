from jasiri import settings
from core.resources import ui_strings as UI_STRINGS


def core_context(request):
    context = {
        "UI_STRINGS": UI_STRINGS,
        'site_name' : settings.SITE_NAME,
        'SITE_NAME' : settings.SITE_NAME,
        'SITE_HEADER_BG': settings.SITE_HEADER_BG,
        'META_KEYWORDS': UI_STRINGS.HOME_META_KEYWORDS,
        'META_DESCRIPTION': UI_STRINGS.HOME_META_DESCRIPTION,
    }
    return context