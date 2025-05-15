from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from ..models import CustomUser, Student, Teacher
from .forms import (
    SetEmailForm,
    UserInfoForm,
    CustomSetPasswordForm,
    ProfileFillStudentForm,
    ProfileFillTeacherFormWithSocNetworks,
)


class SettingsSecurityView(SuccessMessageMixin, LoginRequiredMixin, TemplateView):
    model = CustomUser
    template_name = "education/settings_profile.html"
    success_url = reverse_lazy("users_settings_security")
    login_url = reverse_lazy("login")
    success_message = "Изменения сохранены"

    success_messages = {
        CustomSetPasswordForm.FORM_NAME: "Пароль успешно изменен",
        UserInfoForm.FORM_NAME: "Профиль успешно обновлен",
        SetEmailForm.FORM_NAME: "Email успешно изменен",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if CustomSetPasswordForm.FORM_NAME not in context:
            context[CustomSetPasswordForm.FORM_NAME] = CustomSetPasswordForm(user=user)
        if UserInfoForm.FORM_NAME not in context:
            context[UserInfoForm.FORM_NAME] = UserInfoForm(instance=user)
        if SetEmailForm.FORM_NAME not in context:
            context[SetEmailForm.FORM_NAME] = SetEmailForm(instance=user)

        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        form_name = request.POST.get("form_name")

        if form_name == CustomSetPasswordForm.FORM_NAME:
            form = CustomSetPasswordForm(user, request.POST)
        elif form_name == UserInfoForm.FORM_NAME:
            form = UserInfoForm(request.POST, request.FILES, instance=user)
        elif form_name == SetEmailForm.FORM_NAME:
            form = SetEmailForm(request.POST, instance=user)
        else:
            messages.error(request, "Неизвестная форма")
            return redirect(self.success_url)

        if form.is_valid():
            form.save()
            # TODO: Отправка сообщение в разные формы
            messages.success(request, self.success_messages.get(form_name, self.success_message))
            return redirect(self.success_url)

        context = self.get_context_data()
        context[form.FORM_NAME] = form
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        return self.request.user


class SettingsProfileRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.teacher:
            return reverse_lazy("settings_profile_teacher")
        if self.request.user.student:
            return reverse_lazy("settings_profile_student")
        return reverse_lazy("home")


class SettingsProfileStudentView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Student
    form_class = ProfileFillStudentForm
    template_name = "education/inf_stud.html"
    success_url = reverse_lazy("settings_profile_student")
    success_message = "Профиль успешно обновлен"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not hasattr(request.user, "student"):
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.student


class SettingsProfileTeacherView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Teacher
    form_class = ProfileFillTeacherFormWithSocNetworks
    template_name = "education/inf_teach.html"
    success_url = reverse_lazy("settings_profile_student")
    success_message = "Профиль успешно обновлен"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not hasattr(request.user, "teacher"):
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.teacher
