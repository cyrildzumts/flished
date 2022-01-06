
from blog import forms as BLOG_FORMS
from blog.models import Tag, Category, News, Post, Comment
from blog import constants as Constants
from django.core.cache import cache
from django.db.models import Q, Count, F
from django.template.loader import render_to_string, get_template
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.core.exceptions import ObjectDoesNotExist
from core import core_tools
from flished import utils
import logging

CACHE = cache
logger = logging.getLogger(__name__)


def create_tag(data):
    instance = core_tools.create_instance(model=Tag, data=data)
    if instance:
        logger.info(f"Tag {instance} created")
    
    return instance

def update_tag(tag, data):
    updated_instance = core_tools.update_instance(model=Tag, instance=tag, data=data)
    if updated_instance:
        logger.info(f"Tag {tag} updated")
    
    return updated_instance

def create_news(data):
    news = core_tools.create_instance(model=News, data=data)
    if news:
        logger.info("News created")
    
    return news

def create_comment(data):
    instance = core_tools.create_instance(model=Comment, data=data)
    if instance:
        logger.info("Comment created")
    
    return instance

def update_news(news, data):
    updated_news = core_tools.update_instance(model=News, instance=news, data=data)
    if updated_news:
        logger.info("News updated")
    
    return updated_news


def create_category(data):
    instance = core_tools.create_instance(model=Category, data=data)
    if instance:
        logger.info(f"Category {instance} created")
    
    return instance

def update_category(category, data):
    updated_instance = core_tools.update_instance(model=Category, instance=category, data=data)
    if updated_instance:
        logger.info(f"Category {updated_instance} updated")
    
    return updated_instance

def create_post(data, images=None):
    instance = core_tools.create_instance(model=Post, data=data)
    if instance:
        logger.info(f"Post {instance} created")
    
    return instance

def update_post(post, data, images=None):
    updated_instance = core_tools.update_instance(model=Post, instance=post, data=data)
    if updated_instance:
        logger.info("Post updated")
    
    return updated_instance


def get_post(post_uuid):
    try:
        return Post.objects.get(post_uuid=post_uuid)
    except ObjectDoesNotExist:
        return None

def get_user_posts(user):
    return Post.objects.filter(author=user)

def get_recent_posts():
    return Post.objects.all()[:utils.MAX_RECENTS]

def get_user_recent_posts(user):
    return Post.objects.filter(author=user)[:utils.MAX_RECENTS]


def update_view_count(model, id):
    try:
        model.objects.filter(id=id).update(view_count=F('view_count') + 1)
    except Exception as e:
        logger.warn(f"Error on updating view count for instance of {model} with id \"{id}\"")

def get_category(category_uuid):
    try:
        return Category.objects.get(category_uuid=category_uuid)
    except ObjectDoesNotExist:
        return None


def get_categories():
    categories = CACHE.get(Constants.CACHE_CATEGORY_ALL_PREFIX)
    if categories is None:
        category_queryset = Category.objects.filter(is_active=True)
        categories = [c for c in category_queryset]
        CACHE.set(Constants.CACHE_CATEGORY_ALL_PREFIX, categories )
    return categories




def find_children(root=None):    
    key = Constants.CACHE_CATEGORY_CHILDREN_PREFIX
    if root is None:
        key = Constants.CACHE_CATEGORY_ROOT_CHILDREN_KEY
    else:
        key += root.name
    
    children = CACHE.get(key)
    if children is None:
        category_list = get_categories()
        children = [child for child in category_list if child.parent==root]
        CACHE.set(key, children)

    return children

def make_map(root=None):
    result_map = []
    children = find_children(root)
    if len(children) == 0:
        return []
    
    #logger.debug(f"children Categeries for {root}: {children}")

    for child in children:
        descendants = make_map(child)
        result_map.append({'category': child, 'parent': child.parent, 'children' : descendants })

    return result_map



def build_category_map(root=None):

    key = Constants.CACHE_CATEGORY_MAPS_PREFIX
    if root is None:
        key += 'root'
    else:
        key +=root.name
    category_map = CACHE.get(key)
    if category_map is not None:
        return category_map
    category_map = make_map(root)
    CACHE.set(key, category_map)
    return category_map

    


def fill_category_map_ul(template_name=None):
    template_name = template_name or "tags/navigation_tree.html"
    #cmap = build_category_map()
    cmap = make_map()
    navigation_ul_string = render_to_string(template_name, {'categories_map': cmap})
    return navigation_ul_string


def build_category_paths(category):
    if not isinstance(category, Category):
        return []
    key = Constants.CACHE_CATEGORY_PATH_PREFIX + category.name
    paths = CACHE.get(key)
    if paths is not None:
        return paths
    paths = [category]
    parent = category.parent
    while parent:
        paths.append(parent)
        parent = parent.parent
    paths.reverse()
    CACHE.set(key,paths)
    return paths
    

def get_non_empty_root_category():
    roots = Category.objects.filter(parent=None, is_active=True)
    categories_with_products = Category.objects.exclude(parent=None).annotate(post_count=Count('posts')).filter(post_count__gt=0)
    roots_cats = []
    for c in categories_with_products:
        logger.info(f"Category : {c.name} - {c.display_name} - posts : {c.post_count}" )
    return roots_cats


def category_descendants(category):
    if not isinstance(category, Category):
        return []
    key = Constants.CACHE_CATEGORY_DESCENDANTS_PREFIX + category.name
    descendants = CACHE.get(key)
    if descendants is not None:
        return descendants
    queryset = Category.objects.raw(Constants.CATEGORY_DESCENDANTS_QUERY, [category.id, 'true'])
    descendants = [c for c in queryset]
    CACHE.set(key, descendants)
    return descendants


def category_posts(category):
    if not isinstance(category, Category):
        return []
    key = Constants.CACHE_CATEGORY_POST_PREFIX + category.name
    post_list = CACHE.get(key)
    if post_list is not None:
        return post_list
    queryset = Post.objects.raw(Constants.CATEGORY_POST_QUERY, [category.id])
    post_list = [p for p in queryset]
    CACHE.set(key,post_list)
    return post_list

