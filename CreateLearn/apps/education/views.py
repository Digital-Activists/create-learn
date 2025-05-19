from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin

from .models import Course, Lesson, LessonPage
from .utils import SearchView, TeacherLoginRequired
from .forms import CourseForm, SearchCourseForm


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


class ConstructorCoursesView(TeacherLoginRequired, ListView):
    model = Course
    template_name = "teach_course/teach_course1.html"
    context_object_name = "courses"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = {}

        for course in context["courses"]:
            if course.category not in categories:
                categories[course.category] = []
            categories[course.category].append(course)

        context.update({"categories": categories})
        return context

    def get_queryset(self):
        queryset = Course.objects.filter(creator=self.request.user)
        return queryset.select_related("creator__teacher", "category")


class CreateCourseView(TeacherLoginRequired, SuccessMessageMixin, CreateView):
    model = Course
    template_name = "teach_course/setting_course.html"
    form_class = CourseForm
    success_url = reverse_lazy("teach_create_tasks")
    success_message = "Курс успешно создан"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TeacherSettingsCourse(TeacherLoginRequired, SuccessMessageMixin, UpdateView):
    model = Course
    template_name = "teach_course/setting_course.html"
    form_class = CourseForm
    success_message = "Курс обновлен"
    context_object_name = "course"

    def get_success_url(self):
        slug = self.kwargs.get("slug")  # или self.object.slug
        return reverse_lazy("teach_setting_course", kwargs={"slug": slug})


class TeacherCreateTasks(TeacherLoginRequired, ListView):
    model = LessonPage
    template_name = "teach_course/teach_create_tasks.html"
    context_object_name = "pages"

    def get_queryset(self):
        course_slug = self.kwargs.get("slug")
        module_order = self.kwargs.get("module")
        lesson_order = self.kwargs.get("lesson")

        queryset = LessonPage.objects.filter(
            lesson__module__course__slug=course_slug,
            lesson__module__order=module_order,
            lesson__order=lesson_order,
        ).prefetch_related("attachments")

        if not queryset.exists():
            raise Http404("Урок не найден")

        return queryset.all()


def index(request):
    template_name = "includes/index.html"
    return render(request, template_name)


def about_us(request):
    template_name = "includes/about_us.html"
    return render(request, template_name)
