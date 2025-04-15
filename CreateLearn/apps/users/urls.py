from .views import LoginUserView, RegisterView
from django.urls import include, path
from django.http import HttpResponse

urlpatterns = [
    path("auth/login", LoginUserView.as_view(), name="login"),
    path("auth/register", RegisterView.as_view(), name="register"),
]
