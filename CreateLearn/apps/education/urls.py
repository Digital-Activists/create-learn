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
    #
    # TODO:
    path("my-courses", course1, name="my_courses"),
    # path("constructor/<slug:slug>", view.as_view()),
    # path("constructor/<slug:slug>/lesson/<int:pk>", view.as_view()),
    path("api/", include(router.urls)),
]
