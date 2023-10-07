from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('classifieds/', ClassifiedList.as_view(), name='classified_list'),
    path('classifieds/create', ClassifiedCreate.as_view(), name='classified_create'),
    path('classifieds/<int:pk>', ClassifiedDetail.as_view(), name='classified_detail'),
    path('classifieds/<int:pk>/edit', ClassifiedUpdate.as_view(), name='classified_edit'),
    path('classifieds/<int:pk>/delete/', classified_delete, name='classified_delete'),
    path('replies/', ReplyList.as_view(), name='replies_list'),
    path('classifieds/<int:pk>/reply_create/', reply_create, name='reply_create'),
    path('reply_set_status/', reply_set_status, name='reply_set_status'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/create', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('news/<int:pk>/edit', NewsUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', news_delete, name='news_delete'),
]
