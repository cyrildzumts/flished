from blog import views
from django.conf.urls import url, include
from django.urls import path, reverse_lazy


app_name = "blog"

blog_routes = [
    path('', views.blog_home, name='blog-home'),
    path('new-post/', views.new_post, name="new-post"),
    path('<slug:post_slug>/', views.blog_post, name="blog-post"),
]

urlpatterns = [
    path('', include(blog_routes)),
]
