from django import forms
from ..models import CustomUser, Student, Teacher
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django.core.validators import RegexValidator


class CustomUserCreationForm(UserCreationForm):
    # phone = forms.CharField(
    #     label="Номер телефона",
    #     max_length=20,
    #     validators=[
    #         RegexValidator(
    #             regex=r"^\+?1?\d{9,15}$",
    #             message="Номер должен быть в формате: '+79991234567'. Допускается 9-15 цифр.",
    #         )
    #     ],
    #     widget=forms.TextInput(attrs={"placeholder": "+7 (999) 123-45-67", "type": "tel"}),
    # )

    consent_personal_data_processing = forms.BooleanField(
        label="Согласие на обработку персональных данных",
        required=True,
        widget=forms.CheckboxInput(attrs={}),
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "consent_personal_data_processing",
        )
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "email": "E-mail",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "autofocus": True}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={}),
            "password1": forms.PasswordInput(attrs={"autocomplete": "new-password"}),
            "password2": forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        }


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "id": "email",
                "placeholder": "Ваш e-mail",
                "class": "form-control",
            }
        ),
    )

    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "id": "password",
                "placeholder": "Ваш пароль",
            }
        ),
    )

    def clean_username(self):
        email = self.cleaned_data.get("username")
        return email.lower()  # Нормализуем email к нижнему регистру


class ProfileFillStudentForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        label="Дата рождения", widget=forms.DateInput(attrs={"type": "date"})
    )
    educational_institution = forms.CharField(
        label="Учебное заведение", required=False, max_length=100, widget=forms.TextInput(attrs={})
    )
    course = forms.ChoiceField(
        label="Курс",
        choices=Student.CourseLevel.choices,
        required=False,
        widget=forms.Select(attrs={}),
    )
    class_level = forms.ChoiceField(
        label="Класс",
        choices=Student.ClassLevel.choices,
        required=False,
        widget=forms.Select(attrs={}),
    )

    class Meta:
        model = Student
        fields = ("date_of_birth", "educational_institution", "course", "class_level")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields["date_of_birth"].initial = self.instance.user.date_of_birth

    def save(self, commit=True):
        student = super().save(commit=False)
        student.user.date_of_birth = self.cleaned_data["date_of_birth"]
        if commit:
            student.user.save()
            student.save()
        return student
