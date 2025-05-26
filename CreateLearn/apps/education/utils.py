from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class SearchView(ListView):
    form = None

    # Указать в наследующемся классе следующие поля
    model = None
    template_name = None
    form_class = None
    """Класс для создания формы"""

    def get_queryset(self):
        self.form = self.form_class(self.request.GET or None)
        if self.form.is_valid():
            return self.form.get_results()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form or self.form_class()
        return context


class CustomLoginRequired(LoginRequiredMixin):
    account_type = "teacher"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.user.is_authenticated and not hasattr(request.user, self.account_type):
            return redirect("home")
        return response
