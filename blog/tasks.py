from django.contrib.auth.models import User
from django.db.models import Q,F
from celery import shared_task
from core import constants as CORE_CONSTANTS
from django.utils import timezone
from blog import constants as BLOG_CONSTANTS
from blog.models import Post
import logging


logger = logging.getLogger(__name__)


@shared_task
def publish_scheduled_posts():
    
    NOW = timezone.datetime.now()
    SCHEDULED_FILTER = Q(scheduled_at__lte=NOW) & Q(is_active=True, post_status=BLOG_CONSTANTS.POST_STATUS_SCHEDULED)
    n = Post.objects.filter(SCHEDULED_FILTER).update(post_status=BLOG_CONSTANTS.POST_STATUS_PUBLISHED, published_at=NOW)
    if n:
        logger.info(f"SCHEDULED TASK: Published {n} scheduled publications")
    else:
        logger.info(f"SCHEDULED TASK: No scheduled publications found")