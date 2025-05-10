from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from rest_framework import viewsets

from .serializers import LessonSerializer, CourseSerializer
from .models import Course, Lesson
from .utils import SearchMixin
from .forms import SearchCourseForm


class CoursesListView(SearchMixin):
    model = Course
    form_class = SearchCourseForm
    template_name = "test/test_list.html" 
    context_object_name = "courses"


class CourseDetailView(DetailView):
    model = Course
    template_name = "test/course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context["object"]
        context.update({"lessons": object.lessons.all()})
        return context


class LessonsListView(ListView):
    model = Lesson
    template_name = "test/test_list.html"
    context_object_name = "lessons"

    def get_queryset(self):
        course_slug = self.kwargs.get("course_slug")
        return Lesson.objects.filter(course__slug=course_slug)


class LessonDetailView(DetailView):
    model = Lesson
    template_name = "test/obj_detail.html"
    context_object_name = "lesson"

    def get_object(self, queryset=None):
        course_slug = self.kwargs.get("course_slug")
        module = self.kwargs.get("module")
        order = self.kwargs.get("order")

        lesson = Lesson.objects.filter(
            course__slug=course_slug,
            module=module,
            order=order,
        ).first()

        if not lesson:
            raise Http404("Урок не найден")

        return lesson


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


def index(request):
    template_name = "includes/index.html"
    return render(request, template_name)


def about_us(request):
    template_name = "includes/about_us.html"
    return render(request, template_name)


def course1(request):
    template_name = "teach_course/teach_course1.html"
    return render(request, template_name)
