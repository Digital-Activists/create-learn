from django.shortcuts import render
from django.views.generic import ListView

from .models import Course, Lesson


class CoursesListView(ListView):
    model = Course
    template_name = "base.html"
    context_object_name = "courses"


class CourseDetailView(ListView):
    model = Course
    template_name = "base.html"
    context_object_name = "course"


class LessonsListView(ListView):
    model = Lesson
    template_name = "base.html"
    context_object_name = "lessons"


class LessonDetailView(ListView):
    model = Lesson
    template_name = "base.html"
    context_object_name = "lesson"


def index(request):
    template_name = "includes/index.html"
    return render(request, template_name)
