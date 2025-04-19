from django import forms
from ..models import CustomUser, Student, Teacher
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import (
    AuthenticationForm,
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "middle_name",
            "phone",
            "email",
            "password1",
            "password2",
        )


class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = []


class ProfileFillStudentForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        label="Дата рождения", widget=forms.DateInput(attrs={"type": "date"})
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
    class Meta:
        model = Teacher
        fields = ("about_oneself", "teaching_subjects", "teaching_experience", "qualification")
