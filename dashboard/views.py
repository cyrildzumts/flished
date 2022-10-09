from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied, SuspiciousOperation, ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from dashboard.permissions import PermissionManager, get_view_permissions
from django.contrib import messages
from django.http import Http404
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.db.models import F, Q, Count, Sum
from django.utils import timezone
from rest_framework.authtoken.models import Token
from accounts import constants as Account_Constants
from accounts.forms import AccountCreationForm, UserCreationForm
from accounts import account_services
from dashboard.forms import GroupFormCreation, TokenForm
from blog import blog_service, constants as BLOG_CONSTANTS
from blog.models import Post, Comment, Category, News
from flished import settings, utils
from core.resources import ui_strings as UI_STRINGS

import json

import logging

logger = logging.getLogger(__name__)
# Create your views here.





@login_required
def dashboard(request):
    template_name = "dashboard/dashboard.html"
    username = request.user.username
    can_view_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_view_dashboard :
        logger.warning(f"Dashboard : PermissionDenied to user {username} for path {request.path}")
        raise PermissionDenied
    page_title = UI_STRINGS.DASHBOARD_DASHBOARD_TITLE + ' - ' + settings.SITE_NAME
    now = timezone.now()
    recent_posts = blog_service.get_recent_posts()
    top_10_list = Post.objects.filter(is_active=True).order_by('-view_count')[:utils.TOP_VIEWS_MAX]
    recent_users = User.objects.all().order_by('-date_joined')[:utils.MAX_RECENTS]
    context = {
            'name'          : username,
            'page_title'    : page_title,
            'content_title' : UI_STRINGS.DASHBOARD_DASHBOARD_TITLE,
            'recent_posts': recent_posts,
            'user_list': recent_users,
            'top_10_list': top_10_list,
        }

    logger.info(f"Authorized Access : User {username} has requested the Dashboard Page")

    return render(request, template_name, context)

@login_required
def category_create (request):
    template_name = 'dashboard/category_create.html'
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_add_category(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    if request.method == 'POST':
        category = blog_service.create_category(utils.get_postdata(request))
        if category:
            messages.success(request,_('New Category created'))
            logger.info(f'[ OK ]New Category \"{category.name}\" added by user {request.user.username}' )
            return redirect('dashboard:categories')
        else:
            messages.error(request,_('Error when creating new category'))
            logger.error(f'[ NOT OK ] Error on adding New Category by user {request.user.username}.' )

    page_title = _('New Category')
    context = {
        'page_title': page_title,
        'content_title' : _('New Category'),
        'category_list': Category.objects.all(),
        'SHORT_DESCRIPTION_MAX_SIZE': BLOG_CONSTANTS.SHORT_DESCRIPTION_MAX_SIZE,
        'DESCRIPTION_MAX_SIZE': BLOG_CONSTANTS.DESCRIPTION_MAX_SIZE,
        'SEO_PAGE_TITLE_MAX_SIZE': BLOG_CONSTANTS.SEO_PAGE_TITLE_MAX_SIZE,
        'SEO_DESCRIPTION_MAX_SIZE': BLOG_CONSTANTS.SEO_DESCRIPTION_MAX_SIZE,
        'SEO_META_KEYWORDS_MAX_SIZE': BLOG_CONSTANTS.SEO_META_KEYWORDS_MAX_SIZE,
        'FACEBOOK_DESCRIPTION_MAX_SIZE': BLOG_CONSTANTS.FACEBOOK_DESCRIPTION_MAX_SIZE
    }
    return render(request,template_name, context)
    



@login_required
def categories(request):
    template_name = 'dashboard/category_list.html'
    page_title = _('Category List')
    context = {
        'page_title': page_title,
        'content_title' : _('Categories')
    }
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_view_category(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    queryset = Category.objects.all().order_by('-view_count')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, utils.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['category_list'] = list_set
    return render(request,template_name, context)

@login_required
def category_detail(request, category_uuid=None):
    template_name = 'dashboard/category_detail.html'
    page_title = _('Category')
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_view_category(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    context = {
        'page_title': page_title,
        'SHORT_DESCRIPTION_MAX_SIZE': BLOG_CONSTANTS.SHORT_DESCRIPTION_MAX_SIZE,
        'DESCRIPTION_MAX_SIZE': BLOG_CONSTANTS.DESCRIPTION_MAX_SIZE,
        'SEO_PAGE_TITLE_MAX_SIZE': BLOG_CONSTANTS.SEO_PAGE_TITLE_MAX_SIZE,
        'SEO_DESCRIPTION_MAX_SIZE': BLOG_CONSTANTS.SEO_DESCRIPTION_MAX_SIZE,
        'SEO_META_KEYWORDS_MAX_SIZE': BLOG_CONSTANTS.SEO_META_KEYWORDS_MAX_SIZE,
        'FACEBOOK_DESCRIPTION_MAX_SIZE': BLOG_CONSTANTS.FACEBOOK_DESCRIPTION_MAX_SIZE
    }

    category = get_object_or_404(Category, category_uuid=category_uuid)
    post_list = Post.objects.filter(category__category_uuid=category_uuid)
    context['page_title'] = page_title
    context['category'] = category
    context['post_list'] = post_list
    context['content_title'] = category.display_name
    context['subcategory_list'] = Category.objects.filter(parent=category)
    return render(request,template_name, context)

@login_required
def category_update(request, category_uuid):
    template_name = 'dashboard/category_update.html'
    page_title = _('Edit Category')
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_change_category(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    category = get_object_or_404(Category, category_uuid=category_uuid)
    if request.method == 'POST':
        category  = blog_service.update_category(category, utils.get_postdata(request))
        if category is not None:
            messages.success(request,_('Category updated'))
            logger.info(f'[ OK ] Category \"{category.name}\" updated by user {request.user.username}' )
            return redirect(category.get_dashboard_url())
        else:
            messages.error(request,_('Error when updating category'))
            logger.error(f'[ NOT OK ] Error on updating Category \"{category.name}\" added by user {request.user.username}' )

    
    context = {
        'page_title': page_title,
        'category':category,
        'category_list': Category.objects.exclude(id__in=[category.pk]),
        'content_title': f"{category.display_name} - {_('Update')}",
        'SHORT_DESCRIPTION_MAX_SIZE': BLOG_CONSTANTS.SHORT_DESCRIPTION_MAX_SIZE,
        'DESCRIPTION_MAX_SIZE': BLOG_CONSTANTS.DESCRIPTION_MAX_SIZE,
        'SEO_PAGE_TITLE_MAX_SIZE': BLOG_CONSTANTS.SEO_PAGE_TITLE_MAX_SIZE,
        'SEO_DESCRIPTION_MAX_SIZE': BLOG_CONSTANTS.SEO_DESCRIPTION_MAX_SIZE,
        'SEO_META_KEYWORDS_MAX_SIZE': BLOG_CONSTANTS.SEO_META_KEYWORDS_MAX_SIZE,
        'FACEBOOK_DESCRIPTION_MAX_SIZE': BLOG_CONSTANTS.FACEBOOK_DESCRIPTION_MAX_SIZE
    }
    return render(request,template_name, context)

@login_required
def category_delete(request, category_uuid):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_category(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    if request.method != "POST":
        raise SuspiciousOperation('Bad request. POST request expected but received a GET request')
    category = get_object_or_404(Category, category_uuid=category_uuid)
    Category.objects.filter(pk=category.pk).delete()
    return redirect('dashboard:categories')


@login_required
def categories_delete(request):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_category(request.user):
        logger.warning(f"PermissionDenied to user \"{username}\" for path \"{request.path}\"")
        raise PermissionDenied
    if request.method != "POST":
        raise SuspiciousOperation('Bad request')
    postdata = utils.get_postdata(request)
    id_list = postdata.getlist('categories')

    if len(id_list):
        category_list = list(map(int, id_list))
        Category.objects.filter(id__in=category_list).delete()
        messages.success(request, f"Catergories \"{category_list}\" deleted")
        logger.info(f"Categories \"{category_list}\" deleted by user {username}")
        
    else:
        messages.error(request, f"Catergories  could not be deleted")
        logger.error(f"ID list invalid. Error : {id_list}")
    return redirect('dashboard:categories')


@login_required
def news(request):
    template_name = "dashboard/news_list.html"
    username = request.user.username
    context = {
        'content_title' : UI_STRINGS.DASHBOARD_INFOS_TITLE
    }
    queryset = News.objects.all().order_by('-created_at')
    page_title = _("Infos") + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, utils.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['news_list'] = list_set
    return render(request,template_name, context)



@login_required
def news_create(request):
    template_name = 'dashboard/news_create.html'
    page_title = _('New Infos')
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_add_post(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    context = {
        'page_title': page_title,
        'content_title' : UI_STRINGS.DASHBOARD_INFO_CREATE_TITLE
    }
    if request.method == 'POST':
        postdata = utils.get_postdata(request)
        news = blog_service.create_news(postdata)
        if news:
            messages.success(request,_('Info {news} created'))
            logger.info(f'[ OK ] Info {news} added by user {request.user.username}' )
            return redirect('dashboard:news')
        else:
            messages.error(request,_('Info not created'))
            logger.error(f'[ NOT OK ] Error on adding Info by user {request.user.username}.' )

    return render(request,template_name, context)

@login_required
def news_detail(request, news_uuid=None):
    template_name = 'dashboard/news_detail.html'
    username = request.user.username
    page_title = _('Info')

    news = get_object_or_404(News, news_uuid=news_uuid)
    context = {
        'page_title': page_title,
        'news': news,
        'content_title' : UI_STRINGS.DASHBOARD_INFO_TITLE
    }
    return render(request,template_name, context)


@login_required
def news_update(request, news_uuid=None):
    username = request.user.username
    template_name = 'dashboard/news_update.html'
    page_title = _('Info Update')
    context = {
        'page_title': page_title,
        'content_title' : UI_STRINGS.DASHBOARD_INFO_UPDATE_TITLE
    }
    obj = get_object_or_404(News, news_uuid=news_uuid)
    username = request.user.username
    if request.method == 'POST':
        postdata = utils.get_postdata(request)
        updated_news = blog_service.update_news(obj, postdata)
        if updated_news:
            messages.success(request, _('News updated'))
            logger.info(f'news {updated_news} updated by user \"{username}\"')
            return redirect('dashboard:news-detail', news_uuid=news_uuid)
        else:
            messages.error(request, _('News not updated'))
            logger.error(f'Error on updating news. Action requested by user \"{username}\"')

    context['news'] = obj
    return render(request, template_name, context)


@login_required
def news_delete(request, news_uuid=None):
    username = request.user.username
    obj = get_object_or_404(News, news_uuid=news_uuid)
    News.objects.filter(pk=obj.pk).delete()
    logger.info(f'News \"{obj}\" deleted by user \"{request.user.username}\"')
    messages.success(request, _('News deleted'))
    return redirect('dashboard:news')


@login_required
def news_bulk_delete(request):
    username = request.user.username
    
    postdata = utils.get_postdata(request)
    id_list = postdata.getlist('news-list')

    if len(id_list):
        news_id_list = list(map(int, id_list))
        News.objects.filter(id__in=news_id_list).delete()
        messages.success(request, f"News \"{id_list}\" deleted")
        logger.info(f"News \"{id_list}\" deleted by user {username}")
        
    else:
        messages.error(request, f"News \"{id_list}\" could not be deleted")
        logger.error(f"ID list invalid. Error : {id_list}")
    return redirect('dashboard:news')


##########
@login_required
def posts(request):
    template_name = "dashboard/post_list.html"
    username = request.user.username
    context = {
        'content_title' : UI_STRINGS.DASHBOARD_POSTS_TITLE
    }
    queryset = Post.objects.all().order_by('-created_at')
    page_title = UI_STRINGS.DASHBOARD_POSTS_TITLE + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, utils.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['post_list'] = list_set
    return render(request,template_name, context)



@login_required
def post_create(request):
    template_name = 'dashboard/post_create.html'
    page_title = _('New Post')
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_add_post(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    context = {
        'page_title': page_title,
        'content_title' : UI_STRINGS.DASHBOARD_POST_CREATE_TITLE
    }
    if request.method == 'POST':
        postdata = utils.get_postdata(request)
        instance = blog_service.create_post(postdata)
        if instance:
            messages.success(request,_('Post {instance} created'))
            logger.info(f'[ OK ] Post {instance} added by user {request.user.username}' )
            return redirect('dashboard:posts')
        else:
            messages.error(request,_('Post not created'))
            logger.error(f'[ NOT OK ] Error on adding Post by user {request.user.username}.' )

    return render(request,template_name, context)

@login_required
def post_detail(request, post_uuid=None):
    template_name = 'dashboard/post_detail.html'
    username = request.user.username
    page_title = _('Post')

    instance = get_object_or_404(Post, post_uuid=post_uuid)
    context = {
        'page_title': page_title,
        'blog_post': instance,
        'content_title' : UI_STRINGS.DASHBOARD_POST_TITLE
    }
    return render(request,template_name, context)


@login_required
def post_update(request, post_uuid=None):
    username = request.user.username
    template_name = 'dashboard/post_update.html'
    page_title = _('Post Update')
    context = {
        'page_title': page_title,
        'content_title' : UI_STRINGS.DASHBOARD_INFO_UPDATE_TITLE
    }
    obj = get_object_or_404(Post, post_uuid=post_uuid)
    username = request.user.username
    if request.method == 'POST':
        postdata = utils.get_postdata(request)
        updated_instance = blog_service.update_post(obj, postdata)
        if updated_instance:
            messages.success(request, _('Post updated'))
            logger.info(f'post {updated_instance} updated by user \"{username}\"')
            return redirect('dashboard:post-detail', post_uuid=post_uuid)
        else:
            messages.error(request, _('Post not updated'))
            logger.error(f'Error on updating post. Action requested by user \"{username}\"')

    context['post'] = obj
    return render(request, template_name, context)


@login_required
def post_delete(request, post_uuid=None):
    username = request.user.username
    obj = get_object_or_404(Post, post_uuid=post_uuid)
    Post.objects.filter(pk=obj.pk).delete()
    logger.info(f'Post \"{obj}\" deleted by user \"{request.user.username}\"')
    messages.success(request, _('Post deleted'))
    return redirect('dashboard:posts')


@login_required
def post_bulk_delete(request):
    username = request.user.username
    
    postdata = utils.get_postdata(request)
    id_list = postdata.getlist('posts')

    if len(id_list):
        post_id_list = list(map(int, id_list))
        Post.objects.filter(id__in=post_id_list).delete()
        messages.success(request, f"Posts \"{id_list}\" deleted")
        logger.info(f"Posts \"{id_list}\" deleted by user {username}")
        
    else:
        messages.error(request, f"Posts \"{id_list}\" could not be deleted")
        logger.error(f"ID list invalid. Error : {id_list}")
    return redirect('dashboard:posts')




##########



@login_required
def abtests(request):
    template_name = 'dashboard/abtesting.html'
    page_title = _('AB/TEST')
    
    context = {
        'page_title': page_title,
        'content_title' : page_title,
        #'trackings': ABTest.objects.all()
    }
    
    return render(request, template_name, context)



@login_required
def send_welcome_mail(request, pk):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    user = get_object_or_404(User, pk=pk)
    email_context = {
            'template_name': settings.DJANGO_WELCOME_EMAIL_TEMPLATE,
            'title': 'Bienvenu chez LYSHOP',
            'recipient_email': user.email,
            'context':{
                'SITE_NAME': settings.SITE_NAME,
                'SITE_HOST': settings.SITE_HOST,
                'FULL_NAME': user.get_full_name()
            }
    }
    """send_mail_task.apply_async(
        args=[email_context],
        queue=settings.CELERY_OUTGOING_MAIL_QUEUE,
        routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY
    )"""

    return redirect('dashboard:user-detail', pk=pk)


@login_required
def groups(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_view_group = PermissionManager.user_can_view_group(request.user)
    if not can_view_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    
    #current_account = Account.objects.get(user=request.user)
    group_list = Group.objects.extra(select={'iname':'lower(name)'}).order_by('iname')
    template_name = "dashboard/group_list.html"
    page_title = "Groups" + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(group_list, utils.PAGINATED_BY)
    try:
        group_set = paginator.page(page)
    except PageNotAnInteger:
        group_set = paginator.page(1)
    except EmptyPage:
        group_set = None
    context['page_title'] = page_title
    context['groups'] = group_set

    context['content_title'] = UI_STRINGS.DASHBOARD_GROUPS_TITLE

    return render(request,template_name, context)

@login_required
def group_detail(request, pk=None):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_view_group = PermissionManager.user_can_view_group(request.user)
    if not can_view_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    group = get_object_or_404(Group, pk=pk)
    template_name = "dashboard/group_detail.html"
    page_title = "Group Detail" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['group'] = group
    context['content_title'] = UI_STRINGS.DASHBOARD_GROUP_TITLE

    return render(request,template_name, context)


@login_required
def group_update(request, pk=None):
    # TODO CHECK if the requesting User has the permission to update a group
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_change_group = PermissionManager.user_can_change_group(request.user)
    if not can_change_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = None
    page_title = 'Group Update'
    template_name = 'dashboard/group_update.html'
    group = get_object_or_404(Group, pk=pk)
    form = GroupFormCreation(instance=group)
    group_users = group.user_set.all()
    available_users = User.objects.exclude(pk__in=group_users.values_list('pk'))
    permissions = group.permissions.all()
    available_permissions = Permission.objects.exclude(pk__in=permissions.values_list('pk'))
    if request.method == 'POST':
        form = GroupFormCreation(request.POST, instance=group)
        users = request.POST.getlist('users')
        if form.is_valid() :
            logger.debug("Group form for update is valid")
            if form.has_changed():
                logger.debug("Group has changed")
            group = form.save()
            if users:
                logger.debug("adding %s users [%s] into the group", len(users), users)
                group.user_set.set(users)
            logger.debug("Saved users into the group %s",users)
            return redirect('dashboard:groups')
        else :
            logger.error("Error on editing the group. The form is invalid")
    
    context = {
            'page_title' : page_title,
            'form': form,
            'group': group,
            'users' : group_users,
            'available_users' : available_users,
            'permissions': permissions,
            'available_permissions' : available_permissions,
            'content_title' : UI_STRINGS.DASHBOARD_GROUP_UPDATE_TITLE
    }
    return render(request, template_name, context)


@login_required
def group_create(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_add_group = PermissionManager.user_can_add_group(request.user)
    if not can_add_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = None
    page_title = 'Group Creation'
    template_name = 'dashboard/group_create.html'
    available_permissions = Permission.objects.all()
    available_users = User.objects.all()
    form = GroupFormCreation()
    if request.method == 'POST':
        form = GroupFormCreation(request.POST)
        users = request.POST.getlist('users')
        if form.is_valid():
            logger.debug("Group Create : Form is Valid")
            group_name = form.cleaned_data.get('name', None)
            logger.debug('Creating a Group with the name {}'.format(group_name))
            if not Group.objects.filter(name=group_name).exists():
                group = form.save()
                messages.success(request, "The Group has been succesfully created")
                if users:
                    group.user_set.set(users)
                    logger.debug("Added users into the group %s",users)
                else :
                    logger.debug("Group %s created without users", group_name)

                return redirect('dashboard:groups')
            else:
                msg = "A Group with the given name {} already exists".format(group_name)
                messages.error(request, msg)
                logger.error(msg)
            
        else :
            messages.error(request, "The Group could not be created. Please correct the form")
            logger.error("Error on creating new Group Errors : %s", form.errors)
    
    context = {
            'page_title' : page_title,
            'form': form,
            'available_users' : available_users,
            'available_permissions': available_permissions,
            'content_title' : UI_STRINGS.DASHBOARD_GROUP_CREATE_TITLE
    }

    return render(request, template_name, context)


@login_required
def group_delete(request, pk=None):
    # TODO Check if the user requesting the deletion has the Group Delete permission
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_delete_group = PermissionManager.user_can_delete_group(request.user)
    if not can_delete_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    try:
        group = Group.objects.get(pk=pk)
        name = group.name
        messages.add_message(request, messages.SUCCESS, 'Group {} has been deleted'.format(name))
        group.delete()
        logger.debug("Group {} deleted by User {}", name, request.user.username)
        
    except Group.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Group could not be found. Group not deleted')
        logger.error("Group Delete : Group not found. Action requested by User {}",request.user.username)
        
    return redirect('dashboard:groups')


@login_required
def groups_delete(request):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_group(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if request.method != "POST":
        raise SuspiciousOperation('Bad request. Expected POST request but received a GET')
    
    postdata = utils.get_postdata(request)
    id_list = postdata.getlist('groups')

    if len(id_list):
        instance_list = list(map(int, id_list))
        Group.objects.filter(id__in=instance_list).delete()
        messages.success(request, f"Groups \"{instance_list}\" deleted")
        logger.info(f"Groups \"{instance_list}\" deleted by user {username}")
        
    else:
        messages.error(request, f"Groups could not be deleted")
        logger.error(f"ID list invalid. Error : {id_list}")
    return redirect('dashboard:groups')


@login_required
def create_account(request):
    username = request.user.username
    context = {
        'page_title':_('New User') + ' - ' + settings.SITE_NAME,
    }
    template_name = 'dashboard/new_user.html'
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    can_view_user = PermissionManager.user_can_view_user(request.user)
    can_add_user = PermissionManager.user_can_add_user(request.user)
    if not (can_add_user and can_view_user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    if request.method == 'POST':
        name = request.POST['username']
        result =account_services.AccountService.process_registration_request(request)
        if result['user_created']:
            messages.success(request, _(f"User {name} created"))
            return redirect('dashboard:users')
        else:
            user_form = UserCreationForm(request.POST)
            account_form = AccountCreationForm(request.POST)
            user_form.is_valid()
            account_form.is_valid()
    else:
        user_form = UserCreationForm()
        account_form = AccountCreationForm()
    context['user_form'] = user_form
    context['account_form'] = account_form
    context['content_title'] = UI_STRINGS.DASHBOARD_USER_CREATE_TITLE
    return render(request, template_name, context)



@login_required
def generate_token(request):
    username = request.user.username
    can_view_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_view_dashboard :
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    can_generate_token = PermissionManager.user_can_generate_token(request.user)
    if not can_generate_token:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    template_name = "dashboard/token_generate.html"
    context = {
        'page_title' :_('User Token Generation') + ' - ' + settings.SITE_NAME,
        'can_generate_token' : can_generate_token,
        'content_title' : UI_STRINGS.DASHBOARD_TOKEN_CREATE_TITLE
    }
    if request.method == 'POST':
            form = TokenForm(utils.get_postdata(request))
            if form.is_valid():
                user_id = form.cleaned_data.get('user')
                user = User.objects.get(pk=user_id)
                t = Token.objects.get_or_create(user=user)
                context['generated_token'] = t
                logger.info("user \"%s\" create a token for user \"%s\"", request.user.username, user.username )
                messages.add_message(request, messages.SUCCESS, _(f'Token successfully generated for user {username}') )
                return redirect('dashboard:home')
            else :
                logger.error("TokenForm is invalid : %s\n%s", form.errors, form.non_field_errors)
                messages.add_message(request, messages.ERROR, _('The submitted form is not valid') )
    else :
            context['form'] = TokenForm()
        

    return render(request, template_name, context)

@login_required
def tokens(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    can_view_user = PermissionManager.user_can_view_user(request.user)
    if not can_view_user:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    queryset = Token.objects.all()
    template_name = "dashboard/token_list.html"
    page_title = _("Dashboard Users Tokens") + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, utils.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['token_list'] = list_set
    context['content_title'] =  UI_STRINGS.DASHBOARD_TOKENS_TITLE
    context['can_delete'] = PermissionManager.user_can_delete_user(request.user)
    return render(request,template_name, context)



@login_required
def users(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    can_view_user = PermissionManager.user_can_view_user(request.user)
    if not can_view_user:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    queryset = User.objects.order_by('-date_joined')
    template_name = "dashboard/user_list.html"
    page_title = _("Dashboard Users") + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, utils.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['users'] = list_set
    context['content_title'] = UI_STRINGS.DASHBOARD_USERS_TITLE
    return render(request,template_name, context)



@login_required
def user_details(request, pk=None):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    if not PermissionManager.user_can_view_user(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    context = {}
    #queryset = User.objects.select_related('account')
    user = get_object_or_404(User, pk=pk)
    recent_posts = blog_service.get_user_recent_posts(user)
    template_name = "dashboard/user_detail.html"
    page_title = "User Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['user_instance'] = user
    context['recent_posts'] = recent_posts
    context['content_title'] = f"{UI_STRINGS.DASHBOARD_USER_TITLE} - {user.get_full_name()}"
    return render(request,template_name, context)





@login_required
def users_delete(request):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_user(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if request.method != "POST":
        raise SuspiciousOperation('Bad request. Expected POST request but received a GET')
    
    postdata = utils.get_postdata(request)
    id_list = postdata.getlist('users')

    if len(id_list):
        user_list = list(map(int, id_list))
        User.objects.filter(id__in=user_list).delete()
        messages.success(request, f"Users \"{id_list}\" deleted")
        logger.info(f"Users \"{id_list}\" deleted by user {username}")
        
    else:
        messages.error(request, f"Users \"\" could not be deleted")
        logger.error(f"ID list invalid. Error : {id_list}")
    return redirect('dashboard:users')

@login_required
def user_delete(request, pk=None):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_user(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if request.method != "POST":
        raise SuspiciousOperation('Bad request. Expected POST request but received a GET')
    
    postdata = utils.get_postdata(request)

    User.objects.filter(id=pk).delete()
    messages.success(request, f"Users \"{pk}\" deleted")
    logger.info(f"Users \"{pk}\" deleted by user {username}")
    return redirect('dashboard:users')