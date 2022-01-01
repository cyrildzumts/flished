from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.contrib import messages
from django.db.models import F, Q, Count, Sum
from django.utils import timezone
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
    page_title = _('Dashboard') + ' - ' + settings.SITE_NAME
    now = timezone.now()
    recent_orders = Order.objects.all()[:Constants.MAX_RECENT]
    currents_orders = Order.objects.filter(created_at__year=now.year, created_at__month=now.month)
    recent_products = Product.objects.filter(is_active=True)[:Constants.MAX_RECENT]
    products_count = Product.objects.aggregate(quantity=Sum('quantity')).get('quantity') or 0
    top_10_list = Product.objects.filter(is_active=True).order_by('-view_count')[:Constants.TOP_VIEWS_MAX]
    #recent_sold_products = SoldProduct.objects.all()[:Constants.MAX_RECENT]
    recent_sold_products = CORE_MODELS.SoldProductReport.objects.all()[:Constants.MAX_RECENT]
    recent_users = User.objects.all().order_by('-date_joined')[:Constants.MAX_RECENT]
    facebook_visitors = FacebookLinkHit.objects.aggregate(hits=Sum('hits')).get('hits') or 0
    google_visitors = GoogleAdsHit.objects.aggregate(hits=Sum('hits')).get('hits') or 0
    total_suspicious_visitors = SuspiciousRequest.objects.aggregate(hits=Sum('hits')).get('hits') or 0
    context = {
            'name'          : username,
            'page_title'    : page_title,
            'content_title' : CORE_STRINGS.DASHBOARD_DASHBOARD_TITLE,
            'is_allowed'     : can_view_dashboard,
            'order_list' : recent_orders,
            'currents_orders' : currents_orders,
            'montly_order_count': currents_orders.count(),
            'orders_count': Order.objects.count(),
            'products_count': products_count,
            'users_count' : User.objects.count(),
            'visitors' : Visitor.objects.count(),
            'unique_visitors' : UniqueIP.objects.count(),
            'facebook_visitors' : facebook_visitors,
            'google_visitors' : google_visitors,
            'total_suspicious_visitors': total_suspicious_visitors,
            'product_list': recent_products,
            'sold_product_list': recent_sold_products,
            'user_list': recent_users,
            'top_10_list': top_10_list,
            'active_campaigns' : Campaign.objects.filter(is_active=True)
            #'product_reports' : analytics.report_products(),
            #'online_users': analytics.get_online_users(),
            #'sessions' : Session.objects.all()
        }
    context.update(get_view_permissions(request.user))

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
        category = inventory_service.create_category(utils.get_postdata(request))
        if category:
            messages.success(request,_('New Category created'))
            logger.info(f'[ OK ]New Category \"{category.name}\" added by user {request.user.username}' )
            return redirect('dashboard:categories')
        else:
            messages.error(request,_('Error when creating new category'))
            logger.error(f'[ NOT OK ] Error on adding New Category by user {request.user.username}.' )
    elif request.method == 'GET':
        form = CategoryForm()
    page_title = _('New Category')
    context = {
        'form': form,
        'page_title': page_title,
        'content_title' : _('New Category'),
        'highlight_list':catalog_service.get_highlights({'is_active': True, 'user': None, 'is_home': False}),
        'category_list':models.Category.objects.all(),
        'CATEGORIES':Catalog_Constants.CATEGORIES,
        'SHORT_DESCRIPTION_MAX_SIZE': Catalog_Constants.SHORT_DESCRIPTION_MAX_SIZE,
        'DESCRIPTION_MAX_SIZE': Catalog_Constants.DESCRIPTION_MAX_SIZE,
        'SEO_PAGE_TITLE_MAX_SIZE': Catalog_Constants.SEO_PAGE_TITLE_MAX_SIZE,
        'SEO_DESCRIPTION_MAX_SIZE': Catalog_Constants.SEO_DESCRIPTION_MAX_SIZE,
        'SEO_META_KEYWORDS_MAX_SIZE': Catalog_Constants.SEO_META_KEYWORDS_MAX_SIZE,
        'FACEBOOK_DESCRIPTION_MAX_SIZE': Catalog_Constants.FACEBOOK_DESCRIPTION_MAX_SIZE
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

    queryset = models.Category.objects.all().order_by('-view_count')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, GLOBAL_CONF.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['category_list'] = list_set
    context.update(get_view_permissions(request.user))
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
        'SHORT_DESCRIPTION_MAX_SIZE': Catalog_Constants.SHORT_DESCRIPTION_MAX_SIZE,
        'DESCRIPTION_MAX_SIZE': Catalog_Constants.DESCRIPTION_MAX_SIZE,
        'SEO_PAGE_TITLE_MAX_SIZE': Catalog_Constants.SEO_PAGE_TITLE_MAX_SIZE,
        'SEO_DESCRIPTION_MAX_SIZE': Catalog_Constants.SEO_DESCRIPTION_MAX_SIZE,
        'SEO_META_KEYWORDS_MAX_SIZE': Catalog_Constants.SEO_META_KEYWORDS_MAX_SIZE,
        'FACEBOOK_DESCRIPTION_MAX_SIZE': Catalog_Constants.FACEBOOK_DESCRIPTION_MAX_SIZE
    }

    category = get_object_or_404(models.Category, category_uuid=category_uuid)
    product_list = models.Product.objects.filter(category__category_uuid=category_uuid)
    context['page_title'] = page_title
    context['category'] = category
    context['product_list'] = product_list
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
    category = get_object_or_404(models.Category, category_uuid=category_uuid)
    if request.method == 'POST':
        category , updated = inventory_service.update_category(utils.get_postdata(request), category)
        if updated:
            messages.success(request,_('Category updated'))
            logger.info(f'[ OK ] Category \"{category.name}\" updated by user {request.user.username}' )
            return redirect(category.get_dashboard_url())
        else:
            messages.error(request,_('Error when updating category'))
            logger.error(f'[ NOT OK ] Error on updating Category \"{category.name}\" added by user {request.user.username}' )

    form = CategoryForm(instance=category)
    context = {
        'page_title': page_title,
        'form' : form,
        'category':category,
        'CATEGORIES' : Catalog_Constants.CATEGORIES,
        'category_list': Category.objects.exclude(id__in=[category.pk]),
        'content_title': f"{category.display_name} - {_('Update')}",
        'highlight_list':catalog_service.get_highlights({'is_active': True, 'user': None, 'is_home': False}),
        'SHORT_DESCRIPTION_MAX_SIZE': Catalog_Constants.SHORT_DESCRIPTION_MAX_SIZE,
        'DESCRIPTION_MAX_SIZE': Catalog_Constants.DESCRIPTION_MAX_SIZE,
        'SEO_PAGE_TITLE_MAX_SIZE': Catalog_Constants.SEO_PAGE_TITLE_MAX_SIZE,
        'SEO_DESCRIPTION_MAX_SIZE': Catalog_Constants.SEO_DESCRIPTION_MAX_SIZE,
        'SEO_META_KEYWORDS_MAX_SIZE': Catalog_Constants.SEO_META_KEYWORDS_MAX_SIZE,
        'FACEBOOK_DESCRIPTION_MAX_SIZE': Catalog_Constants.FACEBOOK_DESCRIPTION_MAX_SIZE
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
    category = get_object_or_404(models.Category, category_uuid=category_uuid)
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