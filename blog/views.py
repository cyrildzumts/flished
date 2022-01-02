from django.core.exceptions import BadRequest
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from core.resources import ui_strings as UI_STRINGS
from django.contrib import messages
from blog.models import Post, Category, Tag
from blog import blog_service
from jasiri import utils, settings

import logging


logger = logging.getLogger(__name__)
# Create your views here.


def blog_home(request):
    template_name = "blog/blog_home.html"
    page_title = UI_STRINGS.UI_BLOG_HOME_PAGE_TITLE

    recent_posts = Post.objects.all()[:utils.MAX_RECENTS]
    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
        'recent_posts': recent_posts
    }
    return render(request, template_name, context)


@login_required
def new_post(request):
    template_name = "blog/new_blog_post.html"
    page_title = UI_STRINGS.UI_NEW_BLOG_POST
    if request.method == 'POST':
        logger.info("Post request received")
        utils.show_dict_contents(utils.get_postdata(request), "Blog Post Data")
        return redirect('blog:home')

    recent_posts = []
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
    page_title = f"{post.title} - {settings.SITE_NAME}"
    recent_posts = Post.objects.all()[:utils.MAX_RECENTS]
    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
        'recent_posts': recent_posts,
        'blog_post': post
    }
    return render(request, template_name, context)



def post_preview(request, post_slug):
    template_name = "blog/blog_post_preview.html"

    post = get_object_or_404(Post, slug=post_slug)
    page_title = f"{post.title} - {UI_STRINGS.UI_BLOG_POST_PREVIEW} - {settings.SITE_NAME}"
    context = {
        'page_title': page_title,
        'PAGE_TITLE': page_title,
        'blog_post': post
    }
    return render(request, template_name, context)