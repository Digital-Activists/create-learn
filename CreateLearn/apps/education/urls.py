from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.views.generic.base import RedirectView

from .courses.views import (
    CourseViewSet,
    LessonPageViewSet,
    ModuleViewSet,
    LessonViewSet,
    PageAttachmentViewSet,
)
from .views import (
    CourseDetailView,
    CoursesListView,
    LessonDetailView,
    LessonsListView,
    ConstructorCoursesView,
    index,
    about_us,
    CreateCourseView,
    teach_create_task,
    TeacherSettingsCourse,
)

router = DefaultRouter()
router.register(r"lessons", LessonViewSet)
router.register(r"lesson-pages", LessonPageViewSet)
router.register(r"page-attachments", PageAttachmentViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"modules", ModuleViewSet)

urlpatterns = [
    path("", index, name="home"),
    path("courses", CoursesListView.as_view(), name="education_courses"),
    path("courses/<slug:slug>", CourseDetailView.as_view(), name="course_details"),
    path(
        "courses/<slug:course_slug>/lessons",
        LessonsListView.as_view(),
        name="course_lessons",
    ),
    path(
        "courses/<slug:course_slug>/module/<int:module>/lesson/<int:order>",
        LessonDetailView.as_view(),
        name="lesson_details",
    ),
    path("about_us", about_us, name="education_about_us"),
    path("constructor", RedirectView.as_view(pattern_name="my_courses")),
    path("constructor/my-courses", ConstructorCoursesView.as_view(), name="my_courses"),
    path("constructor/create", CreateCourseView.as_view(), name="teach_course_create"),
    path("constructor/create/tasks", teach_create_task, name="teach_create_tasks"),
    path(
        "constructor/<slug:slug>/setting",
        TeacherSettingsCourse.as_view(),
        name="teach_setting_course",
    ),
    path("api/", include(router.urls)),
]
