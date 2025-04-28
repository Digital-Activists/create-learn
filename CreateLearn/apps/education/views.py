from django.shortcuts import render
from django.views.generic import ListView

from .models import Course, Lesson
from .utils import SearchMixin
from .forms import SearchCourseForm


class CoursesListView(SearchMixin):
    model = Course
    form_class = SearchCourseForm
    template_name = "test/test_list.html"
    # context_object_name = "courses"


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

# страница "О нас"
def about_us(request):
    template_name = "includes/about_us.html"
    return render(request, template_name)
