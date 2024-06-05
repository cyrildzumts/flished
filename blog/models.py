import json
from operator import contains
import sys
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from core.translations.category_strings import CATEGORY_DESCRIPTION_CONTEXT
from blog import constants as Constants
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from flished import settings
import uuid
# Create your models here.
import logging

logger = logging.getLogger(__name__)

def upload_to(instance, filename):
    return f"products/{instance.product.id}/{instance.product.category.code}-{instance.product.id}-{instance.height}x{instance.width}-{filename}"

def upload_post_image_to(instance, filename):
    return f"posts/{instance.slug}/{filename}"


def upload_image_to(instance, filename):
    logger.info(f"Saving image {filename} for instance : {instance} : pk : {instance.pk} - id : {instance.id}")
    return f"posts/images/{instance.pk}/{filename}"

class Tag(models.Model):

    tag = models.CharField(max_length=64)
    tag_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    FORM_FIELDS = ['tag']

    class Meta:
        unique_together = ['tag']
        ordering = ['tag']

    def __str__(self):
        return self.tag
    
    def get_dashboard_url(self):
        return reverse("dashboard:tag-detail", kwargs={"tag_uuid": self.tag_uuid})


    def get_update_url(self):
        return reverse("dashboard:tag-update", kwargs={"tag_uuid": self.tag_uuid})
    

    def get_delete_url(self):
        return reverse("dashboard:tag-delete", kwargs={"tag_uuid": self.tag_uuid})

class Category(models.Model):
    name = models.CharField(max_length=64)
    display_name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addeds_categories', blank=False, null=False)
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(blank=True, null=True, default=0)
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=Constants.CATEGORY_DESCRIPTION_MAX_SIZE, blank=True, null=True)
    seo_page_title = models.CharField(max_length=Constants.SEO_PAGE_TITLE_MAX_SIZE, blank=True, null=True)
    seo_description = models.CharField(max_length=Constants.SEO_DESCRIPTION_MAX_SIZE, blank=True, null=True)
    seo_meta_keywords = models.CharField(max_length=Constants.SEO_META_KEYWORDS_MAX_SIZE, blank=True, null=True)
    facebook_description = models.CharField(max_length=Constants.FACEBOOK_DESCRIPTION_MAX_SIZE, blank=True, null=True)
    category_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    FORM_FIELDS = ['name', 'display_name',  'parent', 'added_by', 'is_active','seo_page_title','seo_description','seo_meta_keywords','facebook_description']

    def __str__(self):
        return f"{self.display_name}"

    
    def get_structured_data(self):
        return {
            '@context': settings.JSON_LD_CONTEXT,
            '@type' : settings.JSON_LD_TYPE_BREADCRUMBLIST,
            'name' : self.display_name,
            'description': self.description,
        }
    
    def get_ctx_title(self):
        if self.name in CATEGORY_DESCRIPTION_CONTEXT:
            return CATEGORY_DESCRIPTION_CONTEXT.get(self.name).get('page-title')
        return self.display_name
    
    
    def get_ctx_description(self):
        if self.name in CATEGORY_DESCRIPTION_CONTEXT:
            return CATEGORY_DESCRIPTION_CONTEXT.get(self.name).get('description')
        return self.description
    
    def get_children(self):
        return Category.objects.filter(parent=self)
    
    """def get_absolute_url(self):
        return reverse("blog:category-detail-old", kwargs={"category_uuid": self.category_uuid})
    
    """
    def get_slug_url(self):
        return reverse("blog:category-detail", kwargs={"slug": self.slug})
    
    def get_dashboard_url(self):
        return reverse("dashboard:category-detail", kwargs={"category_uuid": self.category_uuid})
    
    def get_update_url(self):
        return reverse("dashboard:category-update", kwargs={"category_uuid": self.category_uuid})
    
    def get_delete_url(self):
        return reverse("dashboard:category-delete", kwargs={"category_uuid": self.category_uuid})
    


class Post(models.Model):
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category,related_name='posts', on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="tags", blank=True, null=True)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    #content_draft = models.JSONField(blank=True, null=True)
    content = models.JSONField()
    image = models.ImageField(upload_to=upload_post_image_to, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, blank=True, null=True)
    has_affiliate_link = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    post_status = models.IntegerField(default=Constants.POST_STATUS_DRAFT, blank=True)
    view_count = models.IntegerField(default=0, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="likes")
    readers = models.ManyToManyField(User, related_name="histories", through="PostHistory")
    post_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    FORM_FIELDS = ['author', 'title', 'category', 'content','post_status','image','is_featured', 'has_affiliate_link', 'tags', 'scheduled_at']
    SERIALIZER_FIELDS = ['author', 'title', 'category', 'content', 'post_uuid', 'post_status']
    SEARCH_FIELDS = ['title', 'content']

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

    @property
    def content_json_str(self):
        if self.content is None:
            return None
        return json.dumps(self.content)
    
    def get_absolute_url(self):
        return reverse("blog:blog-post", kwargs={"post_slug": self.slug, 'author': self.author.username})
    
    def get_dashboard_url(self):
        return reverse("dashboard:post-detail", kwargs={"post_uuid": self.post_uuid})
    
    def get_update_url(self):
        return reverse("blog:update-post", kwargs={"post_slug": self.slug})
    
    def get_delete_url(self):
        return reverse("blog:delete-post", kwargs={"post_slug": self.slug})
    

    def save(self, *args, **kwargs):
        if self.image:
            filename,ext = os.path.splitext(self.image.path)
            if ext != Constants.WEBP_EXT:
                name,ext2 = os.path.splitext(self.image.name)
                finale_name = f"{name}{Constants.WEBP_EXT}"
                image = Image.open(self.image)
                image.load()
                img_stream = BytesIO()
                img = image.convert("RGB")
                img.save(img_stream,format="WEBP", quality=Constants.WEBP_QUALITY)
                img_stream.seek(0)
                self.image = InMemoryUploadedFile(img_stream,'ImageField', finale_name, 'image/webp',sys.getsizeof(img_stream),None)

        super(Post, self).save(*args, **kwargs)
    

class PostHistory(models.Model):
    visitor = models.ForeignKey(User, related_name='histroies', on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='histories', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_read = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-last_read']
        constraints = [models.UniqueConstraint(fields=['visitor', 'post'], name="unique_read")]
    
    def __str__(self):
        return f"History - {self.visitor.username} - {self.post.title}"


class News(models.Model):
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=256)
    is_active = models.BooleanField(default=False)
    added_by = models.ForeignKey(User, related_name='added_news', blank=True, null=True, on_delete=models.SET_NULL)
    changed_by = models.ForeignKey(User, related_name='edited_news', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False, editable=False)
    last_changed_at = models.DateTimeField(auto_now=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    news_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    FORM_FIELDS = ['title', 'content', 'is_active', 'added_by', 'changed_by', 'start_at', 'end_at']

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    """def get_absolute_url(self):
        return reverse("dashboard:news-detail", kwargs={"news_uuid": self.news_uuid})
    
    def get_delete_url(self):
        return reverse("dashboard:news-delete", kwargs={"news_uuid": self.news_uuid})

    def get_update_url(self):
        return reverse("dashboard:news-update", kwargs={"news_uuid": self.news_uuid})"""



class Comment(models.Model):

    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='comments', on_delete=models.CASCADE)
    comment = models.CharField(max_length=Constants.COMMENT_MAX_SIZE)
    flags = models.IntegerField(default=0, blank=True, null=True)
    comment_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False, editable=False)
    FORM_FIELDS = ['author', 'comment', 'post']
    SERIALIZER_FIELDS = ['author', 'comment', 'post', 'created_at']

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment - {self.author.username} - {self.post.title}"
    
    def get_dashboard_url(self):
        return reverse("dashboard:comment-detail", kwargs={"comment_uuid": self.comment_uuid})
    

    def get_delete_url(self):
        return reverse("dashboard:tag-delete", kwargs={"comment_uuid": self.comment_uuid})
    




class PostImage(models.Model):
    height = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=64, null=False, blank=False)
    caption = models.CharField(max_length=128, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    image = models.ImageField(upload_to=upload_image_to, height_field='height', width_field='width')
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    last_edited_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    image_uuid = models.UUIDField(default=uuid.uuid4, editable=False)


    def delete_image_file(self):
        self.image.delete(False)

    def get_image_url(self):
        return self.image.url
    
    def get_absolute_url(self):
        return reverse("blog:image-detail", kwargs={"image_uuid": self.image_uuid})
    
    
    def get_update_url(self):
        return reverse("blog:image-update", kwargs={"image_uuid": self.image_uuid})

    def get_delete_url(self):
        return reverse("blog:image-delete", kwargs={"image_uuid": self.image_uuid})


    
    def save(self, *args, **kwargs):
        if self.image:
            filename,ext = os.path.splitext(self.image.path)
            if ext != Constants.WEBP_EXT:
                name,ext2 = os.path.splitext(self.image.name)
                finale_name = f"{name}{Constants.WEBP_EXT}"
                #finale_filename = f"{filename}{constants.WEBP_EXT}"
                image = Image.open(self.image)
                image.load()
                img_stream = BytesIO()
                img = image.convert("RGB")
                img.save(img_stream,format="WEBP", quality=Constants.WEBP_QUALITY)
                img_stream.seek(0)
                self.image = InMemoryUploadedFile(img_stream,'ImageField', finale_name, 'image/webp',sys.getsizeof(img_stream),None)

        super(PostImage, self).save(*args, **kwargs)