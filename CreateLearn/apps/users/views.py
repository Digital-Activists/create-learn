from .models import CustomUser
from .auth.views import (
    LoginUserView,
    logout_user,
    RegisterChoiceView,
    RegisterTeacherView,
    RegisterStudentView,
    ProfileFillStudentView,
    ProfileFillTeacherView,
)
