from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from .modules import Module

User = get_user_model()


class Lesson(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="lessons", verbose_name="Модуль"
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    content = models.TextField(verbose_name="Содержание", blank=True)
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Номер урока")
    is_published = models.BooleanField(default=False)
    # duration_minutes = models.PositiveSmallIntegerField(
    #     verbose_name="Длительность (мин)",
    #     validators=[MaxValueValidator(600)],
    #     blank=True,
    #     null=True,
    # )

    def __str__(self):
        return f"Урок {self.order}: {self.title}"

    def get_absolute_url(self):
        return reverse(
            "lesson_details",
            kwargs={"course_slug": self.module.slug, "module": self.module, "order": self.order},
        )

    class Meta:
        ordering = ["order"]
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        constraints = [
            models.UniqueConstraint(fields=["module", "order"], name="unique_order_per_module")
        ]
        indexes = [
            models.Index(fields=["module", "order"]),
        ]


# Присвоение порядкового номера
@receiver(pre_save, sender=Lesson)
def set_module_order(sender, instance, **kwargs):
    if not instance.pk:  # Если объект создается впервые
        last = Lesson.objects.filter(module=instance.module).order_by("-order").first()
        instance.order = last.order + 1 if last else 0


class UserProgressLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["lesson", "user"], name="unique_lesson_per_user")
        ]

    def save(self, *args, **kwargs):
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)
