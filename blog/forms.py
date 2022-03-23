from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from blog.models import Category, Post, News, Tag, Comment


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = Tag.FORM_FIELDS


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = Category.FORM_FIELDS

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = Comment.FORM_FIELDS
        

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = Post.FORM_FIELDS


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = News.FORM_FIELDS


class FetchCommentsForm(forms.Form):
    created_at = forms.DateTimeField()
    