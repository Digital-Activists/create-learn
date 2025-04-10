from ..models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import (
    AuthenticationForm,
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "phone", "email", "password1", "password2")


class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = []
