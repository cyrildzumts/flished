from django.shortcuts import render
from django.shortcuts import reverse
from django.templatetags.static import static
from flished import settings, utils
from core.resources import ui_strings as UI_STRINGS
from blog import blog_service
import logging

logger = logging.getLogger(__name__)

def page_not_found(request):
    template_name = '404.html'
    return render(request, template_name)


def server_error(request):
    template_name = '500.html'
    return render(request, template_name)

def permission_denied(request):
    template_name = '500.html'
    return render(request, template_name)

def bad_request(request):
    template_name = '500.html'
    return render(request, template_name)


def home(request):
    """
    This function serves the About Page.
    By default the About html page is saved
    on the root template folder.
    """
    template_name = "home.html"
    page_title = f"{UI_STRINGS.HOME_PAGE_TITLE} - {UI_STRINGS.HOME_PAGE_TITLE_LEAD}"
    PAGE_TITLE = page_title
    META_DESCRIPTION = UI_STRINGS.HOME_META_DESCRIPTION
    META_KEYWORDS = UI_STRINGS.HOME_META_KEYWORDS
    context = {
        'page_title': PAGE_TITLE,
        'user_is_authenticated' : request.user.is_authenticated,
        'recent_posts': blog_service.get_recent_posts(),
        'recommendations': blog_service.get_recommendations_post(request.user),
        'main_post': blog_service.get_main_section_posts(request.user),
        'trending': blog_service.get_trending(),
        'kiosk': blog_service.get_category_kiosk(),
        'META_KEYWORDS': META_KEYWORDS,
        'META_DESCRIPTION': META_DESCRIPTION,
        'OG_TITLE' : PAGE_TITLE,
        'OG_DESCRIPTION': META_DESCRIPTION,
        'OG_IMAGE': request.build_absolute_uri(static('flished.png')),
        'OG_URL': request.build_absolute_uri(),
        #'structured_data': structured_data

    }
    return render(request, template_name,context)


def about(request):
    """
    This function serves the About Page.
    By default the About html page is saved
    on the root template folder.
    """
    template_name = "about.html"
    page_title = 'About' + ' - ' + settings.SITE_NAME
    
    
    context = {
        'page_title': page_title,
    }
    return render(request, template_name,context)



def faq(request):
    template_name = "faq.html"
    page_title = "FAQ" + ' - ' + settings.SITE_NAME
    context = {
        'page_title': page_title,
    }
    return render(request, template_name,context)


def privacy_policy(request):
    template_name = "privacy_policy.html"
    page_title =  UI_STRINGS.UI_PRIVACY_POLICY+ ' - ' + settings.SITE_NAME
    context = {
        'page_title': page_title
    }
    return render(request, template_name,context)


def terms_of_use(request):
    template_name = "terms_of_use.html"
    page_title =  UI_STRINGS.UI_TERMS_OF_USE + ' - ' + settings.SITE_NAME
    context = {
        'page_title': page_title
    }
    return render(request, template_name,context)