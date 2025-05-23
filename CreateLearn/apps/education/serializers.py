from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import Course

User = get_user_model()


class BaseStudentsSerializer(serializers.Serializer):
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    emails = serializers.ListField(
        child=serializers.EmailField(),
        min_length=1,
        max_length=50,  # Ограничение на максимальное количество email
    )

    def validate_emails(self, value):
        emails_set = set(email.strip() for email in value if email.strip())
        self.existing_users = User.objects.filter(email__in=emails_set)
        existing_emails = list(self.existing_users.values_list("email", flat=True))
        self.missing_emails = list(emails_set - set(existing_emails))
        return existing_emails

    # TODO: Проверка доступа
    # def validate_course_id(self, value):
    #     if value.owner != self.context["request"].user:
    #         raise serializers.ValidationError("You are not the owner of this course.")
    #     return value


class AddStudentsSerializer(BaseStudentsSerializer):
    def create(self, validated_data):
        course = validated_data["course_id"]
        old_count = course.students.count()
        course.students.add(*self.existing_users)
        added_count = course.students.count() - old_count
        ignored_count = len(self.existing_users) - added_count

        return {
            "course": course.title,
            "added_count": added_count,
            "already_exists_count": ignored_count,
            "missing": {
                "count": len(self.missing_emails),
                "emails": self.missing_emails,
            },
        }


class RemoveUsersSerializer(BaseStudentsSerializer):
    def create(self, validated_data):
        course = validated_data["course_id"]
        old_count = course.students.count()
        course.students.remove(*self.existing_users)
        removed_count = old_count - course.students.count()
        not_enrolled_count = len(self.existing_users) - removed_count

        return {
            "course": course.title,
            "removed_count": removed_count,
            "not_enrolled_count": not_enrolled_count,
            "missing": {
                "count": len(self.missing_emails),
                "emails": self.missing_emails,
            },
        }
