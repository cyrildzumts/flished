from django.core.exceptions import BadRequest, SuspiciousOperation
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.resources import ui_strings as UI_STRINGS
from django.contrib import messages
from blog.forms import PostForm
from blog.models import Post, Category, Tag
from blog import blog_service, constants as Constants
from flished import utils, settings

import logging


logger = logging.getLogger(__name__)
# Create your views here.


def blog_home(request):
    template_name = "blog/blog_home.html"
    page_title = f"{UI_STRINGS.UI_BLOG_HOME_PAGE_TITLE} | {settings.SITE_NAME}"

    recent_posts = Post.objects.all()[:utils.MAX_RECENTS]
    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
        'recent_posts': recent_posts
    }
    return render(request, template_name, context)


@login_required
def create_post(request):
    template_name = "blog/new_blog_post.html"
    page_title = f"{UI_STRINGS.UI_NEW_BLOG_POST} | {settings.SITE_NAME}"
    if request.method == 'POST':
        instance = blog_service.create_post(utils.get_postdata(request))
        return redirect('blog:home')

    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
    }
    return render(request, template_name, context)


@login_required
def create_comment(request, post_slug):
    logger.info(f"New post comment creation request from user {request.user.username}")
    if request.method != 'POST':
        raise BadRequest()
    post = get_object_or_404(Post, slug=post_slug)
    instance = blog_service.create_comment(utils.get_postdata(request))

    return redirect(post.get_absolute_url())


def blog_post(request, post_slug):
    template_name = "blog/blog_post.html"
    post = get_object_or_404(Post, slug=post_slug)
    page_title = f"{post.title} | {settings.SITE_NAME}"
    recent_posts = Post.objects.all()[:utils.MAX_RECENTS]
    blog_service.update_view_count(Post, post.id)
    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
        'recent_posts': recent_posts,
        'blog_post': post,
        'COMMENT_MAX_SIZE': Constants.COMMENT_MAX_SIZE,
    }
    return render(request, template_name, context)


@login_required
def post_preview(request):
    logger.info("previewing post ...")
    template_name = "blog/blog_post_preview.html"
    if request.method != 'POST':
        raise BadRequest()
    form = PostForm(utils.get_postdata(request))
    if not form.is_valid():
        logger.warning(f"Preview Post Error : Invalid form : {form.errors}")
        raise BadRequest()
    post = form.cleaned_data()
    page_title = f"{post.get('title')} - {UI_STRINGS.UI_BLOG_POST_PREVIEW} | {settings.SITE_NAME}"
    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
        'blog_post': post
    }
    return render(request, template_name, context)



def category_detail_slug(request, slug=None):
    template_name = 'catalog/category_detail.html'
    if request.method != 'GET':
        raise SuspiciousOperation

    category = get_object_or_404(Category, slug__iexact=slug, is_active=True)
    
    #subcats = category.get_children().filter(is_active=True)
    subcats = blog_service.find_children(category)
    descendants = blog_service.category_descendants(category)
    queryDict = request.GET.copy()
    queryset = Post.objects.filter(is_active=True, category__in=descendants)
    
    blog_service.update_view_count(Category, category.id)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, utils.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = paginator.page(1)
    paths = blog_service.build_category_paths(category)
    #structured_data = category.get_structured_data()

    PAGE_TITLE = _(category.display_name)
    #META_DESCRIPTION = catalog_service.get_seo_description(category.name,Constants.CATEGORY_DESCRIPTION_KEY, settings.META_DESCRIPTION)
    #META_KEYWORDS = catalog_service.get_seo_description(category.name,Constants.CATEGORY_META_KEYWORDS_KEY, settings.META_KEYWORDS)

    """if subcats:
        structured_data['itemListElement'] = [{'@type':settings.JSON_LD_TYPE_LISTITEM, 'position': index,'name': catalog_service.get_seo_description(cat.name,Constants.CATEGORY_PAGE_TITLE_KEY, default_value=_(cat.display_name)), 'item': settings.SITE_HOST + cat.get_slug_url()} for index, cat in enumerate(subcats,start=1)]
    else:
        structured_data['itemListElement'] = [{'@type':settings.JSON_LD_TYPE_LISTITEM, 'position': index,'name': _(p.display_name), 'item': settings.SITE_HOST + p.get_slug_url()} for index, p in enumerate(queryset[:5],start=1) if p.is_active ]"""

    context = {
        'page_title': PAGE_TITLE,
        'category' : category,
        'parent_category' : category.parent,
        'post_list': list_set,

        'parent_sub_category_list': Category.objects.filter(parent=category.parent, is_active=True),
        'subcategory_list': subcats,
        'subcategories': subcats,
        'OG_TITLE' : PAGE_TITLE,
        'META_DESCRIPTION': UI_STRINGS.HOME_META_DESCRIPTION,
        'META_KEYWORDS': UI_STRINGS.HOME_META_KEYWORDS,
        'OG_DESCRIPTION': UI_STRINGS.HOME_META_DESCRIPTION,
        'CATEGORY_PATHS' : paths,
        'OG_URL': request.build_absolute_uri(),
        'categories_map': blog_service.build_category_map(),
        'CURRENT_CATEGORY_MAP': blog_service.build_category_map(category),
        #'structured_data': structured_data,
    }
    return render(request,template_name, context)