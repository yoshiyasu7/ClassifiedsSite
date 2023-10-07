from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('signup_sent/', signup_sent_view, name='signup_sent'),
    path('<int:pk>/signup_confirmation/', SignUpConfirmation.as_view(), name='signup_confirmation'),
]
