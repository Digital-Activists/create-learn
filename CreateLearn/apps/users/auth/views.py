from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from .forms import CustomUserCreationForm, CustomLoginForm


class RegisterView(CreateView):
    template_name = "base.html"
    success_url = reverse_lazy("home")
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return self.success_url


class LoginUserView(LoginView):
    template_name = "base.html"
    form_class = CustomLoginForm
    success_url = reverse_lazy("home")

    def get_success_url(self):
        return self.success_url


def logout_user(request):
    logout(request)
    return redirect("login")
