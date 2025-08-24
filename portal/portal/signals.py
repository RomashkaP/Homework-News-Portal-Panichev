from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from .models import Post
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='Добро пожаловать на наш портал!',
            message=f'Привет, {instance.username}! Рады видеть тебя!',
            from_email='rilyultash@yandex.ru',
            recipient_list=[instance.email],
        )

@receiver(m2m_changed, sender=Post.categoryes.through)
def notify_on_category_add(sender, instance, action, **kwargs):
    if action == "post_add":
        print(f"Категории добавлены к посту: {instance.categoryes.all()}")
        categories = instance.categoryes.all()
        if categories.exists():
            for category in categories:
                subscribers = category.subscribers.all()
                for user in subscribers:
                    if user.email:
                        try:
                            html_content = render_to_string(
                                'email_message.html', {
                                    'post': instance,
                                    'category': category,
                                    'user': user
                                }
                            )

                            msg = EmailMultiAlternatives(
                                subject='Это сообщение направлено от сиганала',
                                body='',
                                from_email='rilyultash@yandex.ru',
                                to=[user.email]
                            )
                            msg.attach_alternative(html_content, 'text/html')
                            msg.send()

                        except Exception as e:
                            print(f"Ошибка отправки: {e}")


    # if not created:
    #     return
    # categories = instance.categoryes.all()
    # if not categories.exists():
    #     return
    # for category in categories:
    #     subscribers = category.subscribers.all()
    #     if not subscribers.exists():
    #         continue
    #     for user in subscribers:
    #         try:
    #             html_content = render_to_string(
    #                 'email_message.html', {
    #                     'post': instance,
    #                     'category': category,
    #                     'user': user
    #                 }
    #             )
    #
    #             msg = EmailMultiAlternatives(
    #                 subject='Это сообщение направлено от сиганала',
    #                 body='',
    #                 from_email='rilyultash@yandex.ru',
    #                 to=[user.email]
    #             )
    #             msg.attach_alternative(html_content, 'text/html')
    #             msg.send()
    #
    #         except Exception as e:
    #             print(f"Ошибка отправки: {e}")