from blog import views
from django.conf.urls import url, include
from django.urls import path, reverse_lazy


app_name = "blog"

blog_routes = [
    path('', views.stories, name='blog-home'),
    path('create-post/', views.create_post, name="create-post"),
    path('histories/', views.histories, name="histories"),
    path('preview/', views.post_preview, name="post-preview"),

    path('delete/<slug:post_slug>/', views.delete_post, name="delete-post"),
    path('update-post/<slug:post_slug>/', views.update_post, name="update-post"),
    path('create-comment/<slug:author>/<slug:post_slug>/', views.create_comment, name="create-comment"),
    path('categories/<slug:slug>/', views.update_post, name="category-detail"),
    path('<slug:author>/', views.author_stories, name="author-stories"),
    path('<slug:author>/<slug:post_slug>/', views.blog_post, name="blog-post"),
]

urlpatterns = [
    path('', include(blog_routes)),
]
