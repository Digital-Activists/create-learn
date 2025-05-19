from django.db import models

from .lesson import Lesson


class FlashCardsDeck(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="flashcard_decks", verbose_name="Урок"
    )
    title = models.CharField(max_length=200, verbose_name="Название набора")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Набор карточек"
        verbose_name_plural = "Наборы карточек"


class FlashCard(models.Model):
    deck = models.ForeignKey(
        FlashCardsDeck, on_delete=models.CASCADE, related_name="cards", verbose_name="Набор"
    )
    front = models.TextField(verbose_name="Лицевая сторона")
    back = models.TextField(verbose_name="Обратная сторона")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order"]
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"
