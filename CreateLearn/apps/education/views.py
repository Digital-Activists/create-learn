from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AddStudentsSerializer, RemoveUsersSerializer

from .models import Course, Lesson
from .utils import SearchView, CustomLoginRequired, GetQuerysetMixin
from .forms import CoursePeekForm, SearchCourseForm
from .constructor_views import (
    ConstructorCoursesView,
    TeacherCreateQuiz,
    TeacherCreateTasks,
    TeacherSettingsCourse,
    CreateCourseView,
    CreateModuleView,
    CreateLessonView,
)

User = get_user_model()


class CoursesListView(SearchView):
    model = Course
    form_class = SearchCourseForm
    template_name = "education/catalog.html"
    context_object_name = "courses"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("creator__teacher")


class CourseDetailView(DetailView):
    model = Course
    template_name = "education/cart.html"
    context_object_name = "course"


class CourseEnrollView(CustomLoginRequired, DetailView):
    model = Course
    account_type = "student"

    def get(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return redirect("home")  # TODO: redirect на прохождение курса


class CourseDetailExample(TemplateView):
    template_name = "examples/cart.html"


class LessonsListView(ListView):
    model = Lesson
    template_name = "test/test_list.html"
    context_object_name = "lessons"

    def get_queryset(self):
        course_slug = self.kwargs.get("slug")
        return Lesson.objects.filter(course__slug=course_slug)


class LessonDetailView(GetQuerysetMixin, DetailView):
    model = Lesson
    template_name = "test/obj_detail.html"
    context_object_name = "lesson"

    def get_object(self, queryset=None):
        return self.get_object_or_queryset(
            lambda course_slug, module, order: Lesson.objects.filter(
                course__slug=course_slug,
                module=module,
                order=order,
            ),
        )


class UsersPerCourseView(CustomLoginRequired, SuccessMessageMixin, ListView):
    model = User
    template_name = "test/test_list.html"
    context_object_name = "users"
    course_form = CoursePeekForm

    def get_queryset(self):
        queryset = super().get_queryset()
        course_pk = self.request.GET.get("course")

        if course_pk:
            queryset = queryset.filter(pk=course_pk)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.course_form(self.request.GET or None, user=self.request.user)
        return context


class AddStudentsAPIView(APIView):
    def post(self, request, format=None):
        serializer = AddStudentsSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        serializer = RemoveUsersSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    template_name = "includes/index.html"
    return render(request, template_name)


def about_us(request):
    template_name = "includes/about_us.html"
    return render(request, template_name)
