from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.urls import reverse
from blog.models import Post
from core.resources import ui_strings as UI_CORE_STRINGS
from core import renderers
from blog import constants as Constants


class LatestPostsFeed(Feed):
    title = UI_CORE_STRINGS.UI_FEED_TITLE
    link = ""
    description = UI_CORE_STRINGS.UI_FEED_LATEST

    def items(self):
        return Post.objects.filter(post_status=Constants.POST_STATUS_PUBLISHED)[:Constants.FEED_MAX_POST]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return renderers.read_post_summary(item.content)

    """
    def item_link(self, item):
        return item.get_absolute_url()
    """


class AtomPostFeed(LatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description