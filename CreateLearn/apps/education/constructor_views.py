from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model

from .models import Course, LessonPage, Quiz, Module, Lesson
from .utils import CustomLoginRequired, GetQuerysetMixin
from .forms import CourseForm

User = get_user_model()


class ConstructorCoursesView(CustomLoginRequired, ListView):
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


class CreateCourseView(CustomLoginRequired, SuccessMessageMixin, CreateView):
    model = Course
    template_name = "teach_course/setting_course.html"
    form_class = CourseForm
    success_url = reverse_lazy("teach_create_tasks")
    success_message = "Курс успешно создан"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


# TODO: Создание объектов с помощью get запросов - нелогично
class CreateModuleView(CustomLoginRequired, SuccessMessageMixin, DetailView):
    model = Course

    def get(self, request, *args, **kwargs):
        course = self.get_object()
        module = course.modules.create()
        first_lesson = module.lessons.create()
        return redirect("teach_create_tasks", course.slug, module.order, first_lesson.order)


class CreateLessonView(CustomLoginRequired, SuccessMessageMixin, DetailView):
    model = Module

    def get(self, request, *args, **kwargs):
        module = self.get_object()
        lesson = module.lessons.create()
        return redirect("teach_create_tasks", module.course.slug, module.order, lesson.order)

    def get_object(self, queryset=None):
        course_slug = self.kwargs.get("slug")
        module_order = self.kwargs.get("module")
        return Module.objects.filter(course__slug=course_slug, order=module_order).first()


class TeacherSettingsCourse(CustomLoginRequired, SuccessMessageMixin, UpdateView):
    model = Course
    template_name = "teach_course/setting_course.html"
    form_class = CourseForm
    success_message = "Курс обновлен"
    context_object_name = "course"

    def get_success_url(self):
        slug = self.kwargs.get("slug")  # или self.object.slug
        return reverse_lazy("teach_setting_course", kwargs={"slug": slug})


class TeacherCreateTasks(GetQuerysetMixin, CustomLoginRequired, ListView):
    model = LessonPage
    template_name = "teach_course/teach_create_tasks.html"
    context_object_name = "pages"

    def get_queryset(self):
        lesson = self.get_object_or_queryset(
            lambda course_slug, module_order, lesson_order: Lesson.objects.filter(
                module__course__slug=course_slug,
                module__order=module_order,
                order=lesson_order,
            )
        ).first()
        return lesson.pages.all().prefetch_related("attachments")


class TeacherCreateQuiz(GetQuerysetMixin, CustomLoginRequired, DetailView):
    model = Quiz
    template_name = "teach_course/teach_create_card.html"
    context_object_name = "quiz"

    def get_object(self, queryset=None):
        return self.get_object_or_queryset(
            lambda course_slug, module_order, lesson_order: Quiz.objects.filter(
                lesson__module__course__slug=course_slug,
                lesson__module__order=module_order,
                lesson__order=lesson_order,
            ),
        )
