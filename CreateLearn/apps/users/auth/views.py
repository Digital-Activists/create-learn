from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
)

from ..models import Student, Teacher
from .forms import (
    CustomUserCreationForm,
    CustomLoginForm,
    ProfileFillStudentForm,
    ProfileFillTeacherForm,
)


class RegisterChoiceView(TemplateView):
    template_name = "registration/selection_regis.html"


class RegisterBaseView(CreateView):
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return self.success_url


class RegisterStudentView(RegisterBaseView):
    template_name = "registration/stud_regis1.html"
    success_url = reverse_lazy("profile_form_student")

    def form_valid(self, form):
        response = super().form_valid(form)
        Student.objects.create(user=self.object)
        login(self.request, self.object)
        return response


class RegisterTeacherView(RegisterBaseView):
    template_name = "registration/teac-regis1.html"
    success_url = reverse_lazy("profile_form_teacher")

    def form_valid(self, form):
        response = super().form_valid(form)
        Teacher.objects.create(user=self.object)
        login(self.request, self.object)
        return response


class ProfileFillStudentView(LoginRequiredMixin, UpdateView):
    model = Student
    template_name = "test.html"
    success_url = reverse_lazy("home")
    form_class = ProfileFillStudentForm

    def get_object(self, queryset=None):
        return Student.objects.get(user=self.request.user)


class ProfileFillTeacherView(LoginRequiredMixin, UpdateView):
    model = Teacher
    template_name = "test.html"
    success_url = reverse_lazy("home")
    form_class = ProfileFillTeacherForm

    def get_object(self, queryset=None):
        return Teacher.objects.get(user=self.request.user)


class LoginUserView(LoginView):
    template_name = "registration/input.html"
    form_class = CustomLoginForm
    success_url = reverse_lazy("home")

    def get_success_url(self):
        return self.success_url


def logout_user(request):
    logout(request)
    return redirect("login")
