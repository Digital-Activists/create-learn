from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from ..models import CustomUser
from .forms import SetEmailForm, UserInfoForm, CustomSetPasswordForm


class SettingsSecurityView(SuccessMessageMixin, LoginRequiredMixin, TemplateView):
    model = CustomUser
    template_name = "test/test_forms.html"
    success_url = reverse_lazy("users_settings_security")
    login_url = reverse_lazy("login")
    success_message = "Изменения сохранены"

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
            messages.success(request, self.success_message)
            return redirect(self.success_url)

        context = self.get_context_data()
        context[form.FORM_NAME] = form
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        return self.request.user


class SettingsProfileView(LoginRequiredMixin, UpdateView):
    pass
