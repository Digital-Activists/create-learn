from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash

from ..models import CustomUser, Student, Teacher


class CustomSetPasswordForm(SetPasswordForm):
    FORM_NAME = "set_password_form"
    form_name = forms.CharField(widget=forms.HiddenInput(), initial=FORM_NAME, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Настройка виджетов для полей
        self.fields["new_password1"].widget.attrs.update({"placeholder": "Новый пароль"})
        self.fields["new_password2"].widget.attrs.update({"placeholder": "Повторите пароль"})

        # Или так
        # for field in self.fields.values():
        #     field.widget.attrs.update({"class": "form-control"})


class SetEmailForm(forms.ModelForm):
    FORM_NAME = "set_email_form"
    form_name = forms.CharField(widget=forms.HiddenInput(), initial=FORM_NAME, required=False)

    class Meta:
        model = CustomUser
        fields = ["email"]
        widgets = {"email": forms.EmailInput(attrs={"placeholder": "Новый email"})}
        labels = {"email": "Изменить e-mail"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].initial = ""


class UserInfoForm(forms.ModelForm):
    FORM_NAME = "user_info_form"
    form_name = forms.CharField(widget=forms.HiddenInput(), initial=FORM_NAME, required=False)

    class Meta:
        model = CustomUser
        fields = ["avatar", "first_name", "last_name"]
        widgets = {
            "avatar": forms.FileInput(
                attrs={
                    "style": "display: none;",
                    "id": "avatar",
                    "onchange": "previewAvatar(event)",
                }
            ),
            "first_name": forms.TextInput(attrs={"placeholder": "Имя"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Фамилия"}),
        }
        labels = {"first_name": "Имя", "last_name": "Фамилия", "avatar": "Аватар"}


class ProfileFillStudentForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        label="Дата рождения", widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = Student
        fields = ("date_of_birth", "educational_institution", "course", "class_level")
        widgets = {
            "educational_institution": forms.TextInput(attrs={}),
            "course": forms.Select(attrs={}),
            "class_level": forms.Select(attrs={}),
        }
        labels = {}

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
        widgets = {
            "about_oneself": forms.Textarea(
                attrs={
                    "rows": 4,
                }
            ),
            "teaching_subjects": forms.TextInput(attrs={}),
            "teaching_experience": forms.Select(attrs={}),
            "qualification": forms.TextInput(attrs={}),
        }
        labels = {
            "about_oneself": "О себе",
            "teaching_subjects": "Преподаваемые предметы",
            "teaching_experience": "Опыт преподавания",
            "qualification": "Квалификация/Образование",
        }


# TODO: Прикрутка соц сетей
class ProfileFillTeacherFormWithSocNetworks(ProfileFillTeacherForm):
    pass
