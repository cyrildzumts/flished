from django.contrib.sitemaps import Sitemap
from django.templatetags.static import static
from django.shortcuts import reverse



class FlishedSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ["home", "blog:blog-home", "about", "faq", "accounts:login", "accounts:register"]
    
    def location(self, item):
        return reverse(item)