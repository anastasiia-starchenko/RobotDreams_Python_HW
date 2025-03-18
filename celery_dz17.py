import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

app = Celery('myapp')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_course_start_notification_every_day': {
        'task': 'myapp.tasks.send_course_start_notification',
        'schedule': crontab(hour=0, minute=0),
        'args': (1,),
    },
}