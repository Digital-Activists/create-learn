from rest_framework import viewsets

from .course import Course
from .modules import Module
from .lesson import Lesson
from .lesson_page import LessonPage, PageAttachment
from .flash_cards import FlashCardsDeck, FlashCard
from .serializers import (
    LessonSerializer,
    CourseSerializer,
    ModuleSerializer,
    LessonPageSerializer,
    PageAttachmentSerializer,
    FlashCardsDeckSerializer,
    FlashCardSerializer,
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


class FlashCardsDeckViewSet(viewsets.ModelViewSet):
    queryset = FlashCardsDeck.objects.all()
    serializer_class = FlashCardsDeckSerializer


class FlashCardViewSet(viewsets.ModelViewSet):
    queryset = FlashCard.objects.all()
    serializer_class = FlashCardSerializer
