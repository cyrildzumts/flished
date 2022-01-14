from blog import views
from django.conf.urls import url, include
from django.urls import path, reverse_lazy


app_name = "blog"

blog_routes = [
    path('', views.stories, name='blog-home'),
    path('create-post/', views.create_post, name="create-post"),
    path('me/', views.my_stories, name="my-stories"),
    path('preview/', views.post_preview, name="post-preview"),
    path('<slug:author>/', views.author_stories, name="author-stories"),
    path('create-comment/<slug:author>/<slug:post_slug>/', views.create_comment, name="create-comment"),
    path('<slug:author>/<slug:post_slug>/', views.blog_post, name="blog-post"),
]

urlpatterns = [
    path('', include(blog_routes)),
]
