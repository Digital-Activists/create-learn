from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CourseDetailView,
    CourseViewSet,
    CoursesListView,
    LessonDetailView,
    LessonsListView,
    index,
    about_us,
    LessonViewSet,
    course1,
    teach_course_create,
    teach_create_task,
    teach_setting_course,
)

router = DefaultRouter()
router.register(r"lessons", LessonViewSet)
router.register(r"courses", CourseViewSet)

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
    path("my-courses", course1, name="my_courses"),
    path("my-courses/create", teach_course_create, name="teach_course_create"),
    path("my-courses/create/tasks",
         teach_create_task,
         name="teach_create_tasks"),
    path("my-courses/create/setting",
         teach_setting_course,
         name="teach_setting_course"),
    # path("constructor/<slug:slug>", view.as_view()),
    # path("constructor/<slug:slug>/lesson/<int:pk>", view.as_view()),
    path("api/", include(router.urls)),
]
