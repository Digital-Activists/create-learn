from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import Course

User = get_user_model()


class SearchCourseForm(forms.ModelForm):
    def get_results(self):
        if not self.is_valid():
            return Course.objects.none()

        query = Q()

        for field_name, lookup in self.Meta.search_fields.items():
            value = self.cleaned_data.get(field_name)
            if value:
                query &= Q(**{lookup: value})

        return self.Meta.model.objects.filter(query)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.Meta.search_fields.keys():
            self.fields[field_name].required = False

    class Meta:
        model = Course
        fields = ("title",)
        widgets = {
            "title": forms.TextInput(attrs={"type": "search", "placeholder": "Поиск"}),
        }
        search_fields = {
            "title": "title__icontains",
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["avatar", "title", "number_places", "duration", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "text-footer"}),
            "number_palaces": forms.NumberInput(attrs={"class": "text-footer"}),
            "avatar": forms.FileInput(attrs={"style": "display: none;", "id": "avatar-input"}),
            "duration": forms.TextInput(attrs={"class": "text-footer"}),
            "category": forms.Select(attrs={"class": "text-footer"}),
        }


class CoursePeekForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        label="Выберите курс",
        widget=forms.Select(attrs={}),
        empty_label="-- Все курсы --",
        required=False,
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["course"].queryset = Course.objects.filter(creator=user)


class AddUsersToCourseForm(forms.Form):
    """TODO: Класс не используется и не поддерживается"""

    course = forms.ModelChoiceField(queryset=Course.objects.none(), widget=forms.HiddenInput())
    email_1 = forms.EmailField(required=True, label="1")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Можно динамически добавить больше полей
        for i in range(2, 6):
            self.fields[f"email_{i}"] = forms.EmailField(required=False, label=f"{i}")

    def clean(self):
        cleaned_data = super().clean()
        emails = [cleaned_data.get(f"email_{i}") for i in range(1, 6)]
        unique_emails = list(
            email for email in set(emails) if email
        )  # Удаляем дубликаты и пустые строки

        if not unique_emails:
            raise forms.ValidationError("Должен быть указан хотя бы один email")

        if len(unique_emails) != len(emails):
            self.add_warning("Обнаружены повторяющиеся email, они будут обработаны один раз")

        cleaned_data["emails"] = unique_emails
        return cleaned_data
