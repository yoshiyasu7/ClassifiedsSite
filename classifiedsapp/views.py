import os
from pathlib import Path

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, TemplateView
)
from dotenv import load_dotenv

from .models import *
from .filters import NewsFilter, ClassifiedFilter, ReplyFilter
from .forms import ClassifiedFrom, NewsFrom
from .permissions import ChangedPRM
from .signals import news_alert

env_path = Path('../Classifieds') / '.env'
load_dotenv(dotenv_path=env_path)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_pages/profile.html'


class ClassifiedList(ListView):
    model = Classified
    template_name = 'classifieds/classifieds_list.html'
    context_object_name = 'classifieds'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ClassifiedFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ClassifiedDetail(DetailView):
    model = Classified
    template_name = 'classifieds/classifieds_detail.html'
    context_object_name = 'classified'


class ClassifiedCreate(LoginRequiredMixin, CreateView):
    form_class = ClassifiedFrom
    model = Classified
    template_name = 'classifieds/classifieds_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class ClassifiedUpdate(LoginRequiredMixin, ChangedPRM, UpdateView):
    permission_required = ('classifiedsapp.change_classified')
    form_class = ClassifiedFrom
    model = Classified
    template_name = 'classifieds/classifieds_edit.html'


def classified_delete(request):
    pk = request.POST.get('pk')
    classified = Classified.objects.get(pk=pk)
    classified.delete()
    return HttpResponseRedirect('/classifieds/')


class ReplyList(LoginRequiredMixin, ListView):
    model = Reply
    ordering = '-created'
    template_name = 'user_pages/replies_list.html'
    context_object_name = 'replies'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(classified__in=Classified.objects.filter(author=self.request.user)).exclude(status='D')
        self.filterset = ReplyFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


def reply_create(request, pk):
    text = 'test'
    classified = Classified.objects.get(pk=pk)
    user = request.user
    reply = Reply(text=text, classified=classified, author=user)
    reply.save()
    send_mail(
        subject=f"Новый отклик на ваше объявление '{classified.title}'",
        message=f"Уважаемый, {classified.author}!\n\nВы получили новый отклик на ваше объявление '{classified.title}'.\nПримите или отклоните его.",
        from_email=str(os.getenv('DEFAULT_FROM_EMAIL')),
        recipient_list=[classified.author.email]
    )
    return HttpResponseRedirect('/classifieds/')


def reply_set_status(request):
    pk = request.POST.get('pk')
    reply = Reply.objects.get(pk=pk)
    if request.POST.get('accept'):
        reply.status = 'A'
    elif request.POST.get('reject'):
        reply.status = 'D'
    reply.save()
    send_mail(
        subject=f"Реакция на отклик по объявлению '{reply.classified}'",
        message=f"Уважаемый, {reply.author}!\nАвтор объявления '{reply.classified}' ответил на ваш отклик '{reply.text}': {reply.status}.",
        from_email=str(os.getenv('DEFAULT_FROM_EMAIL')),
        recipient_list=[reply.author.email]
    )
    return HttpResponseRedirect('/replies/')


class NewsList(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('classifiedsapp.add_news')
    form_class = NewsFrom
    model = News
    template_name = 'news/news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.author = self.request.user
        news.save()
        news_alert
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, ChangedPRM, UpdateView):
    permission_required = ('classifiedsapp.change_news')
    form_class = NewsFrom
    model = News
    template_name = 'news/news_edit.html'


def news_delete(request):
    pk = request.POST.get('pk')
    news = News.objects.get(pk=pk)
    news.delete()
    return HttpResponseRedirect('/news/')
