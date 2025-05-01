from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from .course import Course

User = get_user_model()


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    content = models.TextField(verbose_name="Содержание", blank=True)
    module = models.PositiveSmallIntegerField(default=0, verbose_name="Номер модуля")
    order = models.PositiveIntegerField(default=0, verbose_name="Номер урока")
    # duration_minutes = models.PositiveSmallIntegerField(
    #     verbose_name="Длительность (мин)",
    #     validators=[MaxValueValidator(600)],
    #     blank=True,
    #     null=True,
    # )

    def __str__(self):
        return f"Модуль: {self.module}. Урок {self.order}: {self.title}"

    def get_absolute_url(self):
        return reverse(
            "lesson_details",
            kwargs={"course_slug": self.course.slug, "module": self.module, "order": self.order},
        )

    class Meta:
        ordering = ["order"]
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        constraints = [
            models.UniqueConstraint(
                fields=["course", "module", "order"], name="unique_lesson_order_per_course"
            )
        ]
        indexes = [
            models.Index(fields=["course", "module", "order"]),
        ]


class LessonAttachment(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="attachments", verbose_name="Урок"
    )
    file = models.FileField(upload_to="lesson_attachments/", verbose_name="Файл")
    # title = models.CharField(max_length=100, verbose_name="Название файла")
    # description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Приложение к уроку"
        verbose_name_plural = "Приложения к урокам"


class UserProgressLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
