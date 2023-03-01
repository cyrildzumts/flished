from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.text import slugify
from blog.models import Category, Post
from core.tasks import send_mail_task
from accounts.models import Account
from flished import settings, utils
import logging
import copy

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def send_welcome_mail(sender, instance, created, **kwargs):
    
    if created:
        logger.info("sending welcome mail ...")
        if str(instance.username).startswith(settings.TEST_USER_PREFIX):
            logger.debug(f"sending welcome mail for test user {instance.username}...")
            return
        title = f'Bienvenu sur {settings.SITE_NAME}'
        email_context = {
            'template_name': settings.DJANGO_WELCOME_EMAIL_TEMPLATE,
            'title': title,
            'recipient_email': instance.email,
            
            'context':{
                'MAIL_TITLE': title,
                'SITE_NAME': settings.SITE_NAME,
                'SITE_HOST': settings.SITE_HOST,
                'FULL_NAME': instance.get_full_name()
            }
        }
        send_mail_task.apply_async(
            args=[email_context],
            queue=settings.CELERY_OUTGOING_MAIL_QUEUE,
            routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY
        )
        admin_email_context = copy.deepcopy(email_context)
        admin_email_context['recipient_email'] = settings.ADMIN_EXTERNAL_EMAIL
        admin_email_context['title'] = "Nouvel utilisateur"
        send_mail_task.apply_async(
            args=[admin_email_context],
            queue=settings.CELERY_OUTGOING_MAIL_QUEUE,
            routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY
        )


@receiver(post_save, sender=Account)
def send_validation_mail(sender, instance, created, **kwargs):
    
    if created:
        logger.info("sending validation mail ...")
        if str(instance.user.username).startswith(settings.TEST_USER_PREFIX):
            logger.debug(f"sending validation mail for test user {instance.user.username} ...")
            return
        logger.info("building email_context")
        email_context = {
            'template_name': settings.DJANGO_VALIDATION_EMAIL_TEMPLATE,
            'title': 'Validation de votre adresse mail',
            'recipient_email': instance.user.email,
            'context':{
                'SITE_NAME': settings.SITE_NAME,
                'SITE_HOST': settings.SITE_HOST,
                'FULL_NAME': instance.user.get_full_name(),
                'MAIL_TITLE': "Validation d'E-Mail",
                'validation_url' : settings.SITE_HOST + instance.get_validation_url()
            }
        }
        logger.info("sending mail task async")
        send_mail_task.apply_async(
            args=[email_context],
            queue=settings.CELERY_OUTGOING_MAIL_QUEUE,
            routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY
        )

@receiver(pre_save, sender=Category)
def generate_category_slug(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)

@receiver(pre_save, sender=Post)
def generate_post_slug(sender, instance, *args, **kwargs):
    instance.slug = slugify( instance.title)