from rest_framework import serializers
from .models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["course", "title", "content", "module", "order"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["title", "description", "creator", "students", "avatar"]
