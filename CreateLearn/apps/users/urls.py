from .views import (
    LoginUserView,
    RegisterChoiceView,
    RegisterTeacherView,
    RegisterStudentView,
    ProfileFillStudentView,
    ProfileFillTeacherView,
    logout_user,
    SettingsProfileView,
    SettingsSecurityView,
)
from django.urls import include, path

urlpatterns = [
    path("auth/logout", logout_user, name="logout"),
    path("auth/login", LoginUserView.as_view(), name="login"),
    path("auth/register/choice", RegisterChoiceView.as_view(), name="register"),
    path("auth/register/teacher", RegisterTeacherView.as_view(), name="register_teacher"),
    path("auth/register/student", RegisterStudentView.as_view(), name="register_student"),
    path(
        "auth/register/profile/student",
        ProfileFillStudentView.as_view(),
        name="profile_form_student",
    ),
    path(
        "auth/register/profile/teacher",
        ProfileFillTeacherView.as_view(),
        name="profile_form_teacher",
    ),
    path(
        "settings/security",
        SettingsSecurityView.as_view(),
        name="users_settings_security",
    ),
    path(
        "settings/profile",
        SettingsProfileView.as_view(),
        name="users_settings_profile",
    ),
]
