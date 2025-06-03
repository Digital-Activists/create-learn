from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from .course import Course

User = get_user_model()


class Module(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="modules", verbose_name="Курс"
    )
    title = models.CharField(max_length=255, verbose_name="Название модуля")
    order = models.PositiveIntegerField(default=0, verbose_name="Номер урока")
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.order}. {self.title}"

    class Meta:
        ordering = ["order"]
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"
        constraints = [
            models.UniqueConstraint(fields=["course", "order"], name="unique_order_per_course")
        ]
        indexes = [
            models.Index(fields=["course", "order"]),
        ]


# Присвоение порядкового номера
@receiver(pre_save, sender=Module)
def set_module_order(sender, instance, **kwargs):
    if not instance.pk:  # Если объект создается впервые
        last = Module.objects.filter(course=instance.course).order_by("-order").first()
        instance.order = last.order + 1 if last else 0


# Вероятно избыточно
# class UserProgressModule(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     module = models.ForeignKey(Module, on_delete=models.CASCADE)
#     is_completed = models.BooleanField(default=False)
#     completed_at = models.DateTimeField(null=True, blank=True)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=["module", "user"], name="unique_module_per_user")
#         ]

#     def save(self, *args, **kwargs):
#         if self.is_completed and not self.completed_at:
#             self.completed_at = timezone.now()
#         super().save(*args, **kwargs)
