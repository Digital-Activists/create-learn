from django.urls import include, path

from .views import CourseDetailView, CoursesListView, LessonDetailView, LessonsListView
from .views import index, about_us

urlpatterns = [
    path("", index, name="home"),
    path("education/courses", CoursesListView.as_view(), name="education_courses"),
    path("education/courses/<slug:slug>", CourseDetailView.as_view()),
    path("education/courses/<slug:slug>/lessons", LessonsListView.as_view(), name="course_lessons"),
    path("education/courses/<slug:slug>/lessons/<int:pk>", LessonDetailView.as_view()),
    path("education/about_us", about_us, name="education_about_us"),
    #
    # TODO:
    # path("education/my-courses", view.as_view(), name="my_courses"),
    # path("education/constructor/<slug:slug>", view.as_view()),
    # path("education/constructor/<slug:slug>/lesson/<int:pk>", view.as_view()),
]
