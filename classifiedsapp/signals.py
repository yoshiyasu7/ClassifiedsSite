import os
from pathlib import Path

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from dotenv import load_dotenv

from .models import News, User

env_path = Path('../Classifieds') / '.env'
load_dotenv(dotenv_path=env_path)


@receiver(post_save, sender=News)
def news_alert(sender, instance, created, **kwargs):
    if created:
        title = f'{instance.title} | {instance.created.strftime("%d %m %Y")}'
        news = News.objects.get(pk=instance.pk)
        users_emails = User.objects.values_list('email', flat=True)

        html_content = render_to_string(
            'news/news_alerts.html',
            {
                'news': news,
                'link': f'{str(os.getenv("SITE_URL"))}/news/{instance.pk}'
            }
        )

        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=str(os.getenv('DEFAULT_FROM_EMAIL')),
            to=users_emails,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print('Уведомление отправлено.')
