from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import SignUpForm, SignUpConfirmationForm


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'sign/signup.html'
    success_url = reverse_lazy('signup_sent')


def signup_sent_view(request):
    context = {}
    logout(request)
    return HttpResponse(render(request, 'sign/signup_email_sent.html', context))


class SignUpConfirmation(UpdateView):
    raise_exception = True
    form_class = SignUpConfirmationForm
    model = User
    template_name = 'sign/signup_confirmation.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.cleaned_data.get('user')
        user.is_active = True
        user_auth = Group.objects.get(name="user_auth")
        user.groups.add(user_auth)
        user.save()
        return response
