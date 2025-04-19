from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Teacher, Student


class StudentInline(admin.StackedInline):
    model = Student
    extra = 0
    can_delete = False
    verbose_name_plural = "Профиль студента"


class TeacherInline(admin.StackedInline):
    model = Teacher
    extra = 0
    can_delete = False
    verbose_name_plural = "Профиль преподавателя"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "last_name",
                    "first_name",
                    "middle_name",
                    "date_of_birth",
                    "password1",
                    "password2",
                    "role",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                    "phone",
                    "date_of_birth",
                    "avatar",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "role",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    ordering = ("email",)

    def get_inline_instances(self, request, obj=None):
        if obj and obj.role == "TEACHER":
            return [TeacherInline(self.model, self.admin_site)]
        elif obj and obj.role == "STUDENT":
            return [StudentInline(self.model, self.admin_site)]
        elif obj and obj.role == "SCHOOL":
            return [SchoolStudentInline(self.model, self.admin_site)]
        return []


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")
