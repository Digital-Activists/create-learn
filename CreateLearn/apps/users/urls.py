from .views import *
from django.urls import include, path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path("", lambda request: HttpResponse("Ok"), name="home"),
    path("auth/login", LoginUserView.as_view(), name="login"),
    path("auth/register", RegisterView.as_view(), name="register"),
    path('', views.index)
]
