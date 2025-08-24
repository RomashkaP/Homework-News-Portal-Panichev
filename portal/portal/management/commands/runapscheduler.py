import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail
from portal.models import Post, Category
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

def my_job():
    now = timezone.now()
    start_of_last_week = now - timedelta(days=now.weekday() + 7)
    end_of_last_week = start_of_last_week + timedelta(days=6)

    categories = Category.objects.all()
    for category in categories:
        posts = Post.objects.filter(
            categoryes__name=category.name,
            time_in__gte=start_of_last_week,
            time_in__lte=end_of_last_week
        )
        if not posts.exists():
            print(f"В категории {category.name} нет постов за прошлую неделю")
            continue
        print(f"Найдено {posts.count()} постов в категории {category.name}")

        subscribers = category.subscribers.all()
        for user in subscribers:
            try:
                html_content = render_to_string(
                    'email_posts_of_last_week.html', {
                        'posts': posts,
                        'category': category,
                        'user': user
                    }
                )
                msg = EmailMultiAlternatives(
                    subject='Это сообщение отправлено из задачника.',
                    body='',
                    from_email='rilyultash@yandex.ru',
                    to=[user.email]
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
            except Exception as e:
                print(f"Ошибка отправки: {e}")

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
        my_job,
        trigger=CronTrigger(day_of_week="mon", hour="8", minute="00"),
        id = "my_job",
        max_instances = 1,
        replace_existing = True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")