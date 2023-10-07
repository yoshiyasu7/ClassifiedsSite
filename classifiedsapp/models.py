import re

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Classified(models.Model):
    CATEGORIES = [
        ('TA', 'Танки'),
        ('HL', 'Хилы'),
        ('DD', 'ДД'),
        ('TR', 'Торговцы'),
        ('GM', 'Гилдмастеры'),
        ('QG', 'Квестгиверы'),
        ('SM', 'Кузнецы'),
        ('TN', 'Кожевники'),
        ('PT', 'Зельевары'),
        ('SP', 'Мастера заклинаний'),
    ]
    title = models.CharField(max_length=255)
    content = RichTextUploadingField('Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=2, choices=CATEGORIES, default='TA')

    def preview(self):
        html_string = str(self.content)
        regexp = re.compile('<.*?>')
        cleaned_string = re.sub(regexp, '', html_string)
        return cleaned_string

    def get_absolute_url(self):
        return reverse('classified_detail', args=[str(self.id)])


class Reply(models.Model):
    STATUSES = [
        ('C', 'Создан'),
        ('A', 'Принят'),
        ('D', 'Отклонён'),
    ]
    text = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUSES, default='C')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text}'


class News(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextUploadingField('Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def preview(self):
        html_string = str(self.content)
        regexp = re.compile('<.*?>')
        cleaned_string = re.sub(regexp, '', html_string)
        return cleaned_string

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])
