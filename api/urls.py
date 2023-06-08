from django.conf.urls import include
from django.urls import path, reverse_lazy
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as drf_api_views
from api import views

app_name = 'api'
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    #path('analytics/', views.analytics_data, name='analytics'),
    path('api-token-auth/', drf_api_views.obtain_auth_token, name='api-token-auth'),
    path('authenticate/', views.authenticate, name='authenticate'),
    path('current-user/', views.get_current_user, name='current-user'),
    path('fetch-credentials/', views.get_credentials, name='fetch-credentials'),
    path('fetchUrl/', views.fetchUrl, name='fetch-url'),
    #path('clear-sessions/', views.clear_sessions, name="clear-sessions"),
    path('create-post/', views.create_post, name='create-post'),
    path('create-tag/', views.create_tag, name='create-tag'),
    path('create-category/', views.create_category, name='create-category'),
    path('create-news/', views.create_news, name='create-news'),
    #path('fetch-payments/', views.fetch_payments, name='api-fetch-payments'),
    #path('verify-coupon/', views.verify_coupon, name='verify-coupon'),
    #path('remove-coupon/', views.remove_coupon_from_cart, name='remove-coupon'),
    #path('update-activity/', views.update_activity, name='update-activity'),
    #path('update-address/<uuid:address_uuid>/', views.update_address, name='update-address'),
    #path('update-campaign/<uuid:campaign_uuid>/', views.update_campaign, name='api-update-campaign'),
    #path('update-highlight/<uuid:highlight_uuid>/', views.update_highlight, name='api-update-highlight'),
    path('add-like/<int:post_id>/', views.add_like, name='add-like'),
    path('remove-like/<int:post_id>/', views.remove_like, name='remove-like'),
    path('update-post/<uuid:post_uuid>/', views.update_post, name='update-post'),
    path('fetch-comments/<int:post_id>/', views.fetch_comments, name='fetch-comments'),

    path('update-tag/<uuid:tag_uuid>/', views.update_tag, name='update-tag'),
    path('update-category/<uuid:category_uuid>/', views.update_category, name='update-category'),
    path('user-search/', views.UserSearchView.as_view(), name="user-search"),
    #path('track-actions/', views.track_user_actions, name='api-track-actions'),
]