from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag, News, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']



class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = Tag.FORM_FIELDS


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = Category.FORM_FIELDS



class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = Post.FORM_FIELDS


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = News.FORM_FIELDS


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = Comment.FORM_FIELDS