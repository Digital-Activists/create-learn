from rest_framework import viewsets

from .course import Course
from .modules import Module
from .lesson import Lesson
from .lesson_page import LessonPage, PageAttachment
from .serializers import (
    LessonSerializer,
    CourseSerializer,
    ModuleSerializer,
    LessonPageSerializer,
    PageAttachmentSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonPageViewSet(viewsets.ModelViewSet):
    queryset = LessonPage.objects.all()
    serializer_class = LessonPageSerializer


class PageAttachmentViewSet(viewsets.ModelViewSet):
    queryset = PageAttachment.objects.all()
    serializer_class = PageAttachmentSerializer
