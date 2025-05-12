from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from .lesson import Lesson

User = get_user_model()


class LessonPage(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="pages", verbose_name="Страница"
    )
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание", blank=True)
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Номер урока")

    def __str__(self):
        return f"Урок {self.order}: {self.title}"

    def get_absolute_url(self):
        return reverse(
            "lesson_details",
            kwargs={"course_slug": self.module.slug, "module": self.module, "order": self.order},
        )

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(fields=["lesson", "order"], name="unique_order_per_lesson")
        ]


class PageAttachment(models.Model):
    page = models.ForeignKey(
        LessonPage, on_delete=models.CASCADE, related_name="attachments", verbose_name="Урок"
    )
    file = models.FileField(upload_to="lesson_attachments/", verbose_name="Файл")
    # title = models.CharField(max_length=100, verbose_name="Название файла")
    # description = models.TextField(blank=True, verbose_name="Описание")


class UserProgressPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(LessonPage, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
