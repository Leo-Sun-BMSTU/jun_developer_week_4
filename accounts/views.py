from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import CreateView

from accounts.forms import UserRegisterForm


class UserSignupView(CreateView):
    """

    """
    model = User
    form_class = UserRegisterForm
    success_url = 'login'
    template_name = 'signup.html'
    success_message = "Your profile was created successfully"


class UserLoginView(LoginView):
    """

    """
    redirect_authenticated_user = True
    template_name = 'login.html'
    success_message = "You are logged in"
