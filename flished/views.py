from django.shortcuts import render
from flished import settings
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
    page_title = f"{settings.SITE_NAME}"
    PAGE_TITLE = page_title
    #META_DESCRIPTION = UI_STRINGS.HOME_META_DESCRIPTION
    #META_KEYWORDS = UI_STRINGS.HOME_META_KEYWORDS
    
    """structured_data = {
            '@context': settings.JSON_LD_CONTEXT,
            '@type' : settings.JSON_LD_TYPE_BREADCRUMBLIST,
            'name' : settings.SITE_NAME,
            'description': str(META_DESCRIPTION),
            'itemListElement' : [{'@type':settings.JSON_LD_TYPE_LISTITEM, 'position': index,'name': catalog_service.get_seo_description(cat.name,Catalog_Constants.CATEGORY_PAGE_TITLE_KEY, default_value=_(cat.display_name)), 'item': settings.SITE_HOST + cat.get_slug_url()} for index, cat in enumerate(catalog_service.find_children()) if cat.is_active]
    }"""

    context = {
        'page_title': PAGE_TITLE,
        'user_is_authenticated' : request.user.is_authenticated,
        'recent_posts': blog_service.get_recent_posts(),
        #'META_KEYWORDS': META_KEYWORDS,
        #'META_DESCRIPTION': META_DESCRIPTION,
        'OG_TITLE' : PAGE_TITLE,
        #'OG_DESCRIPTION': META_DESCRIPTION,
        #'OG_IMAGE': static('assets/lyshop-banner.png'),
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