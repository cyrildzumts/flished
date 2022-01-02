from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from blog import constants as Contants
import uuid
# Create your models here.

def upload_to(instance, filename):
    return f"products/{instance.product.id}/{instance.product.category.code}-{instance.product.id}-{instance.height}x{instance.width}-{filename}"


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
    description = models.CharField(max_length=Contants.CATEGORY_DESCRIPTION_MAX_SIZE, blank=True, null=True)
    seo_page_title = models.CharField(max_length=Contants.SEO_PAGE_TITLE_MAX_SIZE, blank=True, null=True)
    seo_description = models.CharField(max_length=Contants.SEO_DESCRIPTION_MAX_SIZE, blank=True, null=True)
    seo_meta_keywords = models.CharField(max_length=Contants.SEO_META_KEYWORDS_MAX_SIZE, blank=True, null=True)
    facebook_description = models.CharField(max_length=Contants.FACEBOOK_DESCRIPTION_MAX_SIZE, blank=True, null=True)
    category_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    FORM_FIELDS = ['name', 'display_name',  'parent', 'added_by', 'is_active','seo_page_title','seo_description','seo_meta_keywords','facebook_description']

    def __str__(self):
        return f"{self.display_name}"

    
    """def get_structured_data(self):
        return {
            '@context': settings.JSON_LD_CONTEXT,
            '@type' : settings.JSON_LD_TYPE_BREADCRUMBLIST,
            'name' : self.display_name,
            'description': self.description,
        }"""
    
    def get_children(self):
        return Category.objects.filter(parent=self)
    
    """def get_absolute_url(self):
        return reverse("blog:category-detail-old", kwargs={"category_uuid": self.category_uuid})
    
    def get_slug_url(self):
        return reverse("blog:category-detail", kwargs={"slug": self.slug})
    
    def get_dashboard_url(self):
        return reverse("dashboard:category-detail", kwargs={"category_uuid": self.category_uuid})
    
    def get_update_url(self):
        return reverse("dashboard:category-update", kwargs={"category_uuid": self.category_uuid})
    
    def get_delete_url(self):
        return reverse("dashboard:category-delete", kwargs={"category_uuid": self.category_uuid})"""
    


class Post(models.Model):
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category,related_name='posts', on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="tags")
    slug = models.SlugField(max_length=250, blank=True, null=True)
    content = models.JSONField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_status = models.IntegerField(default=Contants.POST_STATUS_DRAFT, blank=True)
    view_count = models.IntegerField(default=0, blank=True, null=True)
    post_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    FORM_FIELDS = ['author', 'title', 'category', 'content']
    SERIALIZER_FIELDS = ['author', 'title', 'category', 'content', 'post_uuid']
    SEARCH_FIELDS = ['title', 'content']

    def __str__(self) -> str:
        return self.title

    
    def get_absolute_url(self):
        return reverse("blog:blog-post", kwargs={"post_slug": self.slug})
    
    """def get_dashboard_url(self):
        return reverse("dashboard:blog-post", kwargs={"slug": self.slug})"""
    


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
    comment = models.CharField(max_length=512)
    flags = models.IntegerField(default=0, blank=True, null=True)
    comment_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False, editable=False)
    FORM_FIELDS = ['author', 'comment', 'post']

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment - {self.author.username} - {self.post.title}"
    
    def get_dashboard_url(self):
        return reverse("dashboard:comment-detail", kwargs={"comment_uuid": self.comment_uuid})
    

    def get_delete_url(self):
        return reverse("dashboard:tag-delete", kwargs={"comment_uuid": self.comment_uuid})