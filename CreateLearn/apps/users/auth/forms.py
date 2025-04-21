from django import forms
from ..models import CustomUser, Student, Teacher
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django.core.validators import RegexValidator


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=150, required=True)
    last_name = forms.CharField(label="Фамилия", max_length=150, required=True)
    # middle_name = forms.CharField(label="Отчество", max_length=150)
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
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={}))
    password1 = forms.CharField(
        label="Пароль",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        required=True,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )
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


class CustomLoginForm(AuthenticationForm):
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    class Meta:
        model = CustomUser
        fields = ["email", "password"]


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
        widget=forms.TextInput(attrs={}),
    )
    class_level = forms.ChoiceField(
        label="Класс",
        choices=Student.ClassLevel.choices,
        required=False,
        widget=forms.TextInput(attrs={}),
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


class ProfileFillTeacherForm(forms.ModelForm):
    about_oneself = forms.CharField(
        label="О себе",
        widget=forms.Textarea(
            attrs={
                "rows": 4,
            }
        ),
        required=False,
        max_length=1000,
    )
    teaching_subjects = forms.CharField(
        label="Преподаваемые предметы",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={}),
    )
    teaching_experience = forms.ChoiceField(
        label="Опыт преподавания",
        choices=Teacher.TeachingExperience.choices,
        required=False,
        widget=forms.TextInput(attrs={}),
    )
    qualification = forms.CharField(
        label="Квалификация/Образование",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={}),
    )

    class Meta:
        model = Teacher
        fields = ("about_oneself", "teaching_subjects", "teaching_experience", "qualification")
