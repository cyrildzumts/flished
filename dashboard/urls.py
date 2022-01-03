from django.conf.urls import url, include
from django.urls import path, reverse_lazy
from dashboard import views

app_name = 'dashboard'


users_patterns = [
    path('', views.dashboard, name='home'),
    path('categories/', views.categories, name='categories'),
    path('categories/detail/<uuid:category_uuid>/', views.category_detail, name='category-detail'),
    path('categories/delete/<uuid:category_uuid>/', views.category_delete, name='category-delete'),
    path('categories/delete/', views.categories_delete, name='categories-delete'),
    path('categories/update/<uuid:category_uuid>/', views.category_update, name='category-update'),

    path('create-account/',views.create_account, name='create-account'),
    path('create-account/',views.create_account, name='create-account'),
    path('generate-token/', views.generate_token, name='generate-token'),
    path('group-create/',views.group_create, name='group-create'),
    path('group-detail/<int:pk>/',views.group_detail, name='group-detail'),
    path('group-delete/<int:pk>/',views.group_delete, name='group-delete'),
    path('group-update/<int:pk>/',views.group_update, name='group-update'),
    path('groups/',views.groups, name='groups'),
    path('groups/delete/',views.groups_delete, name='groups-delete'),

    path('news/',views.news, name='news'),
    path('news/news-create/',views.news_create, name='news-create'),
    path('news/news-detail/<uuid:news_uuid>/',views.news_detail, name='news-detail'),
    path('news/news-delete/<uuid:news_uuid>/',views.news_delete, name='news-delete'),
    path('news/news-update/<uuid:news_uuid>/',views.news_update, name='news-update'),
    path('news/news-bulk-delete/',views.news_bulk_delete, name='news-bulk-delete'),

    path('posts/', views.posts, name='posts'),
    path('posts/detail/<uuid:post_uuid>/', views.post_detail, name='post-detail'),
    #path('posts/post-facebook/<uuid:product_uuid>/', views.product_post_on_facebook, name='product-post-facebook'),
    #path('posts/post-groups-facebook/<uuid:product_uuid>/', views.product_post_on_facebook_groups, name='product-post-groups-facebook'),
    path('posts/update/<uuid:post_uuid>/', views.post_update, name='post-update'),
    path('posts/delete/<uuid:post_uuid>/', views.post_delete, name='post-delete'),
    path('posts/delete/', views.post_bulk_delete, name='posts-delete'),
    path('posts/create/', views.post_create, name='post-create'),
    #path('products/products-changes/', views.products_changes, name='products-changes'),

    path('tokens/', views.tokens, name='tokens'),
    path('users/', views.users, name='users'),
    path('users/create-user/', views.create_account, name='create-user'),
    path('users/detail/<int:pk>/', views.user_details, name='user-detail'),
    path('users/send-welcome-mail/<int:pk>/', views.send_welcome_mail, name='send-welcome-mail'),
    path('users/delete/<int:pk>/', views.user_delete, name='user-delete'),
    path('users/users-delete/', views.users_delete, name='users-delete'),

]