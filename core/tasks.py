from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth.models import User
from django.db.models import Q,F
from celery import shared_task
from django.template.loader import render_to_string
from django.utils import timezone
from blog.models import Category, Post
from flished import settings, utils

import logging


logger = logging.getLogger(__name__)


@shared_task
def send_mail_task(email_context=None):
    logger.info("inside  send_mail_task")
    # TODO : make sending email based on Django Template System.
    if email_context is not None and isinstance(email_context, dict):
        try:
            template_name = email_context['template_name']
        except KeyError as e:
            logger.error(f"send_mail_task : template_name not available. Mail not send. email_context : {email_context}")
            return
        #message = loader.render_to_string(template_name, {'email': email_context})
        root_categories = Category.objects.filter(is_active=True, parent=None)
        context = email_context['context']
        context['root_categories'] = root_categories
        html_message = render_to_string(template_name, context)
        send_mail(
            email_context['title'],
            None,
            settings.DEFAULT_FROM_EMAIL,
            [email_context['recipient_email']],
            html_message=html_message
        )
    else:
        logger.warn(f"send_mail_task: email_context missing or is not a dict. email_context : {email_context}")



@shared_task
def send_publish_mail_task(email_context=None):
    
    # TODO : make sending email based on Django Template System.
    if email_context is not None and isinstance(email_context, dict):

        try:
            template_name = email_context['template_name']
        except KeyError as e:
            logger.error(f"send_order_mail_task : template_name not available. Mail not send. email_context : {email_context}")
            return
        #message = loader.render_to_string(template_name, {'email': email_context})
        root_categories = Category.objects.filter(is_active=True, parent=None)
        post_pk = email_context['post']

        post = Post.objects.select_related().get(pk=post_pk)
        context = email_context['context']
        context['root_categories'] = root_categories
        context['post'] = post
        html_message = render_to_string(template_name, context)
        send_mail(
            email_context['title'],
            None,
            settings.DEFAULT_FROM_EMAIL,
            [email_context['recipient_email']],
            html_message=html_message
        )
    else:
        logger.warn(f"send_order_mail_task: email_context missing or is not a dict. email_context : {email_context}")


@shared_task
def send_mass_mail_task(email_context=None):
    
    # TODO : make sending email based on Django Template System.
    if email_context is not None:

        try:
            template_name = email_context['template_name']
        except KeyError as e:
            logger.debug("template_name not available")
        #message = loader.render_to_string(template_name, {'email': email_context})

        html_message = render_to_string(template_name, email_context['context'])
        messages = ()
        send_mail(
            email_context['title'],
            None,
            settings.DEFAULT_FROM_EMAIL,
            [email_context['recipient_email']],
            html_message=html_message
        )
    else:
        logger.warn("send_mass_mail_task: email_context or recipients not available")

@shared_task
def clean_users_not_actif():
    """
    This Task removes users who have created an account but have not validated their
    E-Mail address. The provided E-Mailaddress is probably an invalid one.
    """
    today = timezone.datetime.today()
    today_date = today.date()
    ACTIVATION_DELAY = today - timezone.timedelta(days=5)
    DATE_JOINED_FILTER = Q(date_joined__lt=ACTIVATION_DELAY) & Q(is_active=False)
    deleted , users= User.objects.filter(DATE_JOINED_FILTER).delete()
    logger.info(f"Clean User inactifs : deleted {deleted} inactive users {users}")