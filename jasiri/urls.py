"""jasiri URL Configuration

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
from django.conf.urls import url, include
from django.conf.urls.static import static
from jasiri import views, settings


urlpatterns = i18n_patterns( * [
    path('', views.home, name="home"),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
    #path('api/', include('api.urls', namespace='api')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('faq/', views.faq, name='faq'),
    #path('dashboard/', include('dashboard.urls')),

])

urlpatterns +=[
    path('i18n/', include('django.conf.urls.i18n')),
    #path('api/', include('api.urls', namespace='api')),
    #path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('privacy-policy/', views.privacy_policy, name="privacy-policy"),
    #path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path('terms-of-use/', views.terms_of_use, name="terms-of-use"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
