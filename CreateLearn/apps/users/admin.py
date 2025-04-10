from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Teacher, Student, SchoolStudent


class StudentInline(admin.StackedInline):
    model = Student
    extra = 0
    can_delete = False
    verbose_name_plural = "Профиль студента"


class SchoolStudentInline(admin.StackedInline):
    model = SchoolStudent
    extra = 0
    can_delete = False
    verbose_name_plural = "Профиль школьника"


class TeacherInline(admin.StackedInline):
    model = Teacher
    extra = 0
    can_delete = False
    verbose_name_plural = "Профиль преподавателя"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
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


@admin.register(SchoolStudent)
class SchoolStudentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")
