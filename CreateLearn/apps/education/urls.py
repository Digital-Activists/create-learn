from django.urls import include, path

from .views import CourseDetailView, CoursesListView, LessonDetailView, LessonsListView
from .views import index

urlpatterns = [
    path("education/courses", CoursesListView.as_view(), name="courses"),
    path("education/courses/<slug:slug>", CourseDetailView.as_view()),
    path("education/courses/<slug:slug>/lessons", LessonsListView.as_view(), name="lessons"),
    path("education/courses/<slug:slug>/lessons/<int:pk>", LessonDetailView.as_view()),
    path("", index, name="home"),
]
