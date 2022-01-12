from blog import views
from django.conf.urls import url, include
from django.urls import path, reverse_lazy


app_name = "blog"

blog_routes = [
    path('', views.blog_home, name='blog-home'),
    path('create-post/', views.create_post, name="create-post"),
    path('create-comment/<slug:post_slug>/', views.create_comment, name="create-comment"),
    path('<slug:post_slug>/', views.blog_post, name="blog-post"),
    path('preview/', views.post_preview, name="post-preview"),
]

urlpatterns = [
    path('', include(blog_routes)),
]
