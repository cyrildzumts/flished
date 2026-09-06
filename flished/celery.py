from kombu import Exchange, Queue
from flished import settings
from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flished.settings')
app = Celery(settings.SITE_NAME)
app.config_from_object('django.conf:settings', namespace=settings.CELERY_NAMESPACE)
app.conf.task_acks_late = True
app.conf.task_default_queue_type = 'quorum'
app.conf.task_reject_on_worker_lost = True
app.conf.control_queue_exclusive = True
app.conf.event_queue_exclusive = True
app.conf.worker_enable_remote_control = False
app.conf.task_create_missing_queues=True
app.conf.task_create_missing_queue_type="quorum"
app.conf.task_create_missing_queue_exchange_type="topic"
# # Add this to handle connection loss with Quorum queues
app.conf.broker_transport_options = {
    'confirm_publish': True,
    'queue_properties': {
        'x-queue-type': 'quorum'
    }
}
app.conf.result_backend_transport_options = {
    'confirm_publish': True,
    'queue_properties': {
        'x-queue-type': 'quorum'
    }
}

DEFAULT_QUEUES_ARGS = {
    'x-queue-type': 'quorum'
}

app.conf.task_queues = (
    Queue(settings.CELERY_DEFAULT_QUEUE, Exchange(settings.CELERY_DEFAULT_EXCHANGE), routing_key=settings.CELERY_DEFAULT_ROUTING_KEY, queue_arguments=DEFAULT_QUEUES_ARGS),
    Queue(settings.CELERY_OUTGOING_MAIL_QUEUE, Exchange(settings.CELERY_OUTGOING_MAIL_EXCHANGE), routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY, queue_arguments=DEFAULT_QUEUES_ARGS),
    Queue(settings.CELERY_IDENTIFICATION_QUEUE, Exchange(settings.CELERY_IDENTIFICATION_EXCHANGE), routing_key=settings.CELERY_IDENTIFICATION_ROUTING_KEY, queue_arguments=DEFAULT_QUEUES_ARGS),
    Queue(settings.CELERY_LOGGER_QUEUE, Exchange(settings.CELERY_LOGGER_EXCHANGE), routing_key=settings.CELERY_LOGGER_ROUTING_KEY, queue_arguments=DEFAULT_QUEUES_ARGS),
)
app.conf.beat_schedule = {
    'clean_users': {
        'task': 'core.tasks.clean_users_not_actif',
        'schedule' : crontab(minute=0, hour=0)

    },
    'scheduled_posts': {
        'task': 'blog.tasks.publish_scheduled_posts',
        'schedule' : crontab(minute="*/15", hour="*")

    },
}
app.autodiscover_tasks()