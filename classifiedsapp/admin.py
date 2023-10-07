from django.contrib import admin
from .models import *


class ClassifiedsAdmin(admin.ModelAdmin):
    model = Classified
    list_display = ('title', 'category', 'content', 'author')
    list_filter = ('author', 'category')
    search_fields = ('title', 'content')


class ReplyAdmin(admin.ModelAdmin):
    model = Reply
    list_display = ('text', 'status', 'classified', 'author', 'created')
    list_filter = ('status', 'author')
    search_fields = ('text', 'classified')


class NewsAdmin(admin.ModelAdmin):
    model = News
    list_display = ('title', 'content', 'author', 'created')
    list_filter = ('author', )
    search_fields = ('title', 'content')


# Register your models here.
admin.site.register(Classified, ClassifiedsAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(News, NewsAdmin)
