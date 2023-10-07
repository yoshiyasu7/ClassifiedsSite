import django_filters as df
from django.forms import DateInput, TextInput

from .models import *


class ClassifiedFilter(df.FilterSet):
    author = df.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Автор',
        empty_label='Все авторы'
    )

    category = df.ChoiceFilter(choices=Classified.CATEGORIES)

    title = df.CharFilter(
        lookup_expr='icontains',
        label='Заголовок',
        widget=TextInput(attrs={'placeholder': 'Поиск по названию'})
    )

    content = df.CharFilter(
        lookup_expr='icontains',
        label='Содержание объявления',
    )

    class Meta:
        model = Classified
        fields = ['author', 'category', 'title', 'content']


class ReplyFilter(df.FilterSet):
    author = df.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Автор',
        empty_label='Все авторы'
    )

    created = df.DateFilter(
        lookup_expr='gte',
        label='Дата отклика',
        widget=DateInput(attrs={'type': 'date'}),
    )

    classified = df.ModelChoiceFilter(
        queryset=Classified.objects.all(),
        label='Объявление',
        empty_label='Все объявления'
    )

    status = df.ChoiceFilter(choices=Reply.STATUSES)

    class Meta:
        model = Reply
        fields = ['author', 'created', 'classified', 'status']


class NewsFilter(df.FilterSet):
    created = df.DateFilter(
        lookup_expr='gte',
        label='Дата публикации',
        widget=DateInput(attrs={'type': 'date'}),
    )

    title = df.CharFilter(
        lookup_expr='icontains',
        label='Заголовок',
        widget=TextInput(attrs={'placeholder': 'Поиск по названию'})
    )

    author = df.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Автор',
        empty_label='Все авторы'
    )

    content = df.CharFilter(
        lookup_expr='icontains',
        label='Содержание',
        widget=TextInput(attrs={'placeholder': 'Поиск по содержанию'})
    )

    class Meta:
        model = News
        fields = ['created', 'title', 'author', 'content']
