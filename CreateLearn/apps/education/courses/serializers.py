from rest_framework import serializers
from .course import Course
from .lesson import Lesson
from .modules import Module
from .lesson_page import LessonPage, PageAttachment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["module", "title", "content", "order", "is_published"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "title",
            "category",
            "description",
            "creator",
            "students",
            "avatar",
            "is_published",
            "duration",
            "number_places",
        ]


class PageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageAttachment
        fields = ["page", "file"]


class LessonPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPage
        fields = ["lesson", "title", "order", "content"]


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["course", "title", "order", "is_published"]
