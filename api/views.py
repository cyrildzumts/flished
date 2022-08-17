from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework import filters
from rest_framework.generics import ListAPIView
from django.contrib.auth.models import User
from api import serializers
from api.serializers import PostSerializer, UserSerializer, TagSerializer, CategorySerializer, CommentSerializer, NewsSerializer
from flished import utils
from blog import blog_service
from core import core_tools, load_credentials
from core.resources import ui_strings as UI_STRINGS

import logging
import uuid
import json
logger = logging.getLogger(__name__)

# Create your views here.
class UserSearchByNameView(ListAPIView):
     #permission_classes = [IsAuthenticated]
     serializer_class = UserSerializer
     search_fields = ['last_name', 'first_name','username']
     filter_backends = [filters.SearchFilter]
     queryset = User.objects.filter(is_superuser=False)
     


class UserSearchView(ListAPIView):
     #permission_classes = [IsAuthenticated]
     serializer_class = UserSerializer
     search_fields = ['last_name', 'first_name', 'username']
     filter_backends = [filters.SearchFilter]
     queryset = User.objects.filter(is_superuser=False)


@api_view(['GET'])
def get_current_user(request):
    if request.user.is_authenticated:
        data = {'username': request.user.username, 'user_id': request.user.pk, 'last_login': request.user.last_login, 'is_valid':True}
    else:
        data = {'username': 'anonymous user', 'user_id': -1, 'is_valid':False}
    return Response(data)



@api_view(['POST'])
def create_post(request):
    logger.info(f"API: New post creation request from user {request.user.username}")
    if request.method != 'POST':
        return Response({'status': False, 'errror': 'Bad request. Use POST instead'}, status=status.HTTP_400_BAD_REQUEST)
    
    instance = blog_service.create_post(utils.get_postdata(request), utils.get_uploaded_files(request))
    data = None
    if instance is None:
        data = {
            'success': False,
            'message': "Invalid data"
        }
    else:
        serializer = PostSerializer(instance)
        data = {
            'success': True,
            'message': 'Post created',
            'post': serializer.data,
            'url': instance.get_absolute_url()
        }
    
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_comment(request):
    logger.info(f"API: New post comment creation request from user {request.user.username}")
    if request.method != 'POST':
        return Response({'status': False, 'errror': 'Bad request. Use POST instead'}, status=status.HTTP_400_BAD_REQUEST)
    
    instance = blog_service.create_comment(utils.get_postdata(request))
    data = None
    if instance is None:
        data = {
            'success': False,
            'message': "Invalid data"
        }
    else:
        serializer = CommentSerializer(instance)
        data = {
            'success': True,
            'message': 'Comment created',
            'comment': serializer.data
        }
    
    return Response(data=data, status=status.HTTP_200_OK)



@api_view(['POST'])
def update_post(request, post_uuid):
    logger.info(f"API: Update post request from user {request.user.username}")
    if request.method != 'POST':
        return Response({'status': False, 'errror': 'Bad request. Use POST instead'}, status=status.HTTP_400_BAD_REQUEST)
    post = blog_service.get_post(post_uuid)
    if post is None:
        return Response(data={'success': False, 'message': UI_STRINGS.UI_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
    instance = blog_service.update_post(post, utils.get_postdata(request), utils.get_uploaded_files(request))
    data = None
    if instance is None:
        data = {
            'success': False,
            'message': "Invalid data"
        }
    else:
        serializer = PostSerializer(instance)
        data = {
            'success': True,
            'message': 'Post created',
            'post': serializer.data,
            'url': instance.get_absolute_url()
        }
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([])
def add_like(request, post_id):
    if request.method != 'POST':
        return Response({'status': False, 'errror': 'Bad request. Use POST instead'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = blog_service.add_like(post_id, request.user)
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([])
def remove_like(request, post_id):
    if request.method != 'POST':
        return Response({'status': False, 'errror': 'Bad request. Use POST instead'}, status=status.HTTP_400_BAD_REQUEST)
    data = blog_service.remove_like(post_id, request.user)
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([])
def fetch_comments(request, post_id):
    if request.method != 'POST':
        return Response({'status': False, 'errror': 'Bad request. Use POST instead'}, status=status.HTTP_400_BAD_REQUEST)
    data = blog_service.get_new_post_comments(post_id, utils.get_postdata(request))
    if data.get('not_found', False):
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_category(request):
    logger.info(f"API: New post creation request from user {request.user.username}")
    if request.method != 'POST':
        return Response({'status': False, 'errror': 'Bad request. Use POST instead'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = blog_service.create_post(utils.get_postdata(request))
    
    return Response(data=data, status=status.HTTP_200_OK)



@api_view(['POST'])
def update_category(request, category_uuid):
    logger.info(f"API: Update category request from user {request.user.username}")
    if request.method != 'POST':
        return Response({'status': False, 'errror': 'Bad request. Use POST instead'}, status=status.HTTP_400_BAD_REQUEST)
    category = blog_service.get_category(category_uuid)
    if category is None:
        return Response(data={'success': False, 'message': UI_STRINGS.UI_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
    data = blog_service.update_category(category, utils.get_postdata(request))
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_tag(request):
    logger.info(f"API: New tag creation request from user {request.user.username}")
    if request.method != 'POST':
        return Response({'status': False, 'errror': 'Bad request. Use POST instead'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = blog_service.create_tag(utils.get_postdata(request))
    
    return Response(data=data, status=status.HTTP_200_OK)



@api_view(['POST'])
def update_tag(request, tag_uuid):
    logger.info(f"API: Update category request from user {request.user.username}")
    if request.method != 'POST':
        return Response({'status': False, 'errror': 'Bad request. Use POST instead'}, status=status.HTTP_400_BAD_REQUEST)
    tag = blog_service.get_tag(tag_uuid)
    if tag is None:
        return Response(data={'success': False, 'message': UI_STRINGS.UI_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
    data = blog_service.update_tag(tag, utils.get_postdata(request))
    return Response(data=data, status=status.HTTP_200_OK)



@api_view(['POST'])
def create_news(request):
    logger.info(f"API: New news creation request from user {request.user.username}")
    if request.method != 'POST':
        return Response({'status': False, 'errror': 'Bad request. Use POST instead'}, status=status.HTTP_400_BAD_REQUEST)
    
    data = blog_service.create_new(utils.get_postdata(request))
    
    return Response(data=data, status=status.HTTP_200_OK)



@api_view(['POST'])
def update_news(request, news_uuid):
    logger.info(f"API: Update news request from user {request.user.username}")
    if request.method != 'POST':
        return Response({'status': False, 'errror': 'Bad request. Use POST instead'}, status=status.HTTP_400_BAD_REQUEST)
    news = blog_service.get_news(news_uuid)
    if news is None:
        return Response(data={'success': False, 'message': UI_STRINGS.UI_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
    data = blog_service.update_news(news, utils.get_postdata(request))
    return Response(data=data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def authenticate(request):
    logger.debug("Received authenticate request")
    postdata = request.POST.copy()
    utils.show_dict_contents(postdata, "API Athenticate Header")
    token = uuid.uuid4()
    return Response(data={"tokenType": 'Bearer', 'accessToken': token}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def get_credentials(request):
    logger.debug("Received credential request")
    postdata = request.POST.copy()
    credential = load_credentials.load_unsplash_credentials()
    return Response(data=credential, status=status.HTTP_200_OK)


@api_view(['POST'])
def clear_sessions(request):
    logger.debug("Received Clear sessions request")
    cleared = True
    return Response(data={"cleared": cleared}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def update_activity(request):
    postdata = request.POST.copy()
    return Response(data={'success': True, 'message': 'updated'}, status=status.HTTP_200_OK)


@api_view()
def fetchUrl(request):
    data = core_tools.core_fetch_url(request.GET.copy().get("url"))
    return Response(data)