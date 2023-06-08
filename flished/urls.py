"""flished URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from flished.sitemaps import FlishedSiteMap
from flished import views, settings
from blog import views as blog_views, sitemaps as blog_sitemaps, feeds as blog_feeds

sitemaps = {
    'static' : FlishedSiteMap,
    'publications': blog_sitemaps.PostSiteMap
}

urlpatterns_i18n = i18n_patterns( * [
    path('', views.home, name="home"),
    path('about/', views.about, name='about'),
    path('accounts/', include('accounts.urls')),
    path('stories/', include('blog.urls', namespace='blog')),
    path('me/',blog_views.my_stories,name='me'),
    path('faq/', views.faq, name='faq'),
    path('dashboard/', include('dashboard.urls')),
    path('scheduled/', blog_views.scheduled_stories, name="scheduled"),
    path('search/', blog_views.search, name="search"),


], prefix_default_language=False)

urlpatterns =[
    path('api/', include('api.urls', namespace='api')),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('privacy-policy/', views.privacy_policy, name="privacy-policy"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path('terms-of-use/', views.terms_of_use, name="terms-of-use"),
    path('i18n/', include('django.conf.urls.i18n')),
    path('feeds/rss/', blog_feeds.LatestPostsFeed()),
    path('feeds/atom/', blog_feeds.AtomPostFeed()),
    *urlpatterns_i18n
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
