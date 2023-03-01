from django.contrib.sitemaps import Sitemap
from blog import constants as Contants
from blog.models import Post, Category


class CategorySiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Category.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.created_at
    
    def location(self, item):
        return item.get_slug_url()



class PostSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Post.objects.filter(is_active=True, post_status=Contants.POST_STATUS_PUBLISHED)
    
    def lastmod(self, obj):
        return obj.created_at
    
    def location(self, item):
        return item.get_absolute_url()