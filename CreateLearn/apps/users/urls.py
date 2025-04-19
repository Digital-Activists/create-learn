from .views import (
    LoginUserView,
    RegisterChoiceView,
    RegisterTeacherView,
    RegisterStudentView,
    ProfileFillStudentView,
    ProfileFillTeacherView,
)
from django.urls import include, path
from django.http import HttpResponse

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r"users", UserViewSet)

urlpatterns = [
    # path("users", include(router.urls)),
    path("users/auth/login", LoginUserView.as_view(), name="login"),
    path("users/auth/register/choice", RegisterChoiceView.as_view(), name="register"),
    path("users/auth/register/teacher", RegisterTeacherView.as_view(), name="register_teacher"),
    path("users/auth/register/student", RegisterStudentView.as_view(), name="register_student"),
    path(
        "users/auth/register/profile/student",
        ProfileFillStudentView.as_view(),
        name="profile_form_student",
    ),
    path(
        "users/auth/register/profile/teacher",
        ProfileFillTeacherView.as_view(),
        name="profile_form_teacher",
    ),
]
