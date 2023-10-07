from django import forms
from .models import Classified, News, Reply


class ClassifiedFrom(forms.ModelForm):
    """Форма объявлений"""
    class Meta:
        model = Classified
        fields = ['title', 'content', 'category', ]


class NewsFrom(forms.ModelForm):
    """Форма новостей"""
    class Meta:
        model = News
        fields = ['title', 'content', ]
