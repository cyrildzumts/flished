from django.core.exceptions import BadRequest, SuspiciousOperation
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.resources import ui_strings as UI_STRINGS
from core import renderers
from django.contrib import messages
from blog.forms import PostForm
from blog.models import Post, Category, Tag
from blog import blog_service, constants as Constants
from flished import utils, settings, conf as GLOBAL_CONF
import datetime
import logging


logger = logging.getLogger(__name__)
# Create your views here.


def stories(request):
    template_name = "blog/blog_home.html"
    page_title = f"{UI_STRINGS.UI_BLOG_HOME_PAGE_TITLE} | {settings.SITE_NAME}"

    queryset = Post.objects.filter(post_status=Constants.POST_STATUS_PUBLISHED, is_active=True)
    recommendations = blog_service.get_recommendations_post(request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, GLOBAL_CONF.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = paginator.page(1)
    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
        'story_list': list_set,
        'recommendations': recommendations
    }
    return render(request, template_name, context)


def author_stories(request,author):
    template_name = "blog/blog_home.html"
    page_title = f"{UI_STRINGS.UI_BLOG_HOME_PAGE_TITLE} | {settings.SITE_NAME}"

    queryset = Post.objects.filter(post_status=Constants.POST_STATUS_PUBLISHED, author__username=author, is_active=True)
    posts_count = queryset.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, GLOBAL_CONF.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = paginator.page(1)
    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
        'story_list': list_set,
        'posts_count': posts_count,
    }
    return render(request, template_name, context)

@login_required
def my_stories(request):
    template_name = "blog/me.html"
    page_title = f"{UI_STRINGS.UI_BLOG_HOME_PAGE_TITLE} | {settings.SITE_NAME}"

    queryset = Post.objects.filter(author=request.user)
    posts_count = queryset.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, GLOBAL_CONF.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = paginator.page(1)
    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
        'story_list': list_set,
        'SHOW_STATUS': True,
        'posts_count': posts_count,
    }
    return render(request, template_name, context)


@login_required
def scheduled_stories(request):
    template_name = "blog/scheduled.html"
    page_title = f"{UI_STRINGS.UI_BLOG_HOME_PAGE_TITLE} | {settings.SITE_NAME}"

    queryset = Post.objects.filter(author=request.user, post_status=Constants.POST_STATUS_SCHEDULED)
    posts_count = queryset.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, GLOBAL_CONF.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = paginator.page(1)
    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
        'story_list': list_set,
        'SHOW_STATUS': True,
        'posts_count': posts_count
    }
    return render(request, template_name, context)


@login_required
def histories(request):
    template_name = "blog/history.html"
    page_title = f"{UI_STRINGS.UI_READ_HISTORY_PAGE_TITLE} | {settings.SITE_NAME}"

    queryset = blog_service.get_histories(request.user)
    posts_count = queryset.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, GLOBAL_CONF.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = paginator.page(1)
    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
        'histories': list_set,
        'posts_count': posts_count,
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
        'LOAD_EDITOR': True,
    }
    return render(request, template_name, context)


@login_required
def update_post(request, post_slug):
    template_name = "blog/blog_post_update.html"
    post = get_object_or_404(Post, slug=post_slug, author=request.user)
    images = []
    if post.image:
        images.append(post.image)
    page_title = f"{post.title} | {UI_STRINGS.UI_UPDATE_BLOG_POST} | {settings.SITE_NAME}"
    if request.method == 'POST':
        instance = blog_service.update_post(utils.get_postdata(request))
        return redirect('blog:home')

    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
        'post': post,
        'images': images,
        'LOAD_EDITOR': True,
    }
    return render(request, template_name, context)


@login_required
def create_comment(request,author, post_slug):
    logger.info(f"New post comment creation request from user {request.user.username}")
    if request.method != 'POST':
        raise BadRequest()
    post = get_object_or_404(Post, slug=post_slug, author__username=author)
    instance = blog_service.create_comment(utils.get_postdata(request))

    return redirect(post.get_absolute_url())




def blog_post(request, author, post_slug):
    template_name = "blog/blog_post.html"
    post = get_object_or_404(Post, slug=post_slug, author__username=author)
    page_title = f"{post.title} | {settings.SITE_NAME}"
    liked = False
    SHOW_STATUS: False
    if request.user.is_authenticated:
        liked = post.likes.filter(id=request.user.pk).exists()
        blog_service.add_read_history(request.user, post)
        SHOW_STATUS = request.user == post.author
    recent_posts = Post.objects.all()[:GLOBAL_CONF.MAX_RECENT]
    post_comments = post.comments.all()
    if post_comments.exists():
        latest = post_comments.last().created_at.isoformat()
    else:
        latest = datetime.datetime.now().isoformat()
    blog_service.update_view_count(Post, post.id)
    
    image_url = None
    if post.image:
        image_url = f"{settings.SITE_HOST}{post.image.url}"
    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
        'OG_TITLE': page_title,
        'META_DESCRIPTION': renderers.read_post_summary(post.content),
        'OG_URL': request.build_absolute_uri(),
        'OG_IMAGE': image_url,
        'OG_WEBSITE': 'article',
        'recent_posts': recent_posts,
        'POST_STATUS_DRAFT': Constants.POST_STATUS_DRAFT,
        'POST_DELETED': post.post_status == Constants.POST_STATUS_DELETED,
        'blog_post': post,
        'comments': post_comments,
        'LIKED': liked,
        'latest': latest,
        'LIKES': post.likes.count(),
        'SHOW_STATUS': SHOW_STATUS,
        'COMMENT_MAX_SIZE': Constants.COMMENT_MAX_SIZE,
    }
    return render(request, template_name, context)


@login_required
def delete_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, author=request.user)
    Post.objects.filter(pk=post.pk).update(post_status=Constants.POST_STATUS_DELETED)
    return redirect('blog:blog-home')


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
    post = form.cleaned_data
    page_title = f"{post.get('title')} - {UI_STRINGS.UI_BLOG_POST_PREVIEW} | {settings.SITE_NAME}"
    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
        'blog_post': post
    }
    return render(request, template_name, context)



def category_detail_slug(request, slug=None):
    template_name = 'blog/category.html'
    if request.method != 'GET':
        raise SuspiciousOperation

    category = get_object_or_404(Category, slug__iexact=slug, is_active=True)
    
    subcats = blog_service.find_children(category)
    descendants = blog_service.category_descendants(category)
    queryDict = request.GET.copy()
    queryset = Post.objects.filter(is_active=True,post_status=Constants.POST_STATUS_PUBLISHED, category__in=descendants)
    
    blog_service.update_view_count(Category, category.id)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, GLOBAL_CONF.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = paginator.page(1)
    paths = blog_service.build_category_paths(category)
    #structured_data = category.get_structured_data()

    PAGE_TITLE = _(category.display_name)
    
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