from django.db import models
from django.contrib.auth import get_user_model

from .lesson import Lesson

User = get_user_model()


class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name="quiz")
    # title = models.CharField(max_length=200, verbose_name="Название теста")
    # passing_score = models.PositiveSmallIntegerField(
    #     default=80,
    #     verbose_name="Проходной балл (%)",
    #     validators=[MinValueValidator(1), MaxValueValidator(100)],
    # )
    # attempts_limit = models.PositiveSmallIntegerField(
    #     default=3, verbose_name="Лимит попыток", null=True, blank=True
    # )

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class QuestionKind(models.TextChoices):
    SINGLE_CHOICE = "SINGLE", "Одиночный выбор"
    MULTIPLE_CHOICE = "MULTIPLE", "Множественный выбор"
    MATCHING = "MATCHING", "Сопоставление"
    # TEXT_ANSWER = "TEXT", "Текстовый ответ"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(verbose_name="Текст вопроса", blank=True)
    order = models.PositiveIntegerField(default=0)
    kind = models.CharField(
        max_length=10,
        choices=QuestionKind.choices,
        default=QuestionKind.SINGLE_CHOICE,
        verbose_name="Вид вопроса",
    )
    # points = models.PositiveSmallIntegerField(
    #     default=1,
    #     verbose_name="Баллы за вопрос"
    # )
    # explanation = models.TextField(
    #     blank=True,
    #     verbose_name="Объяснение ответа"
    # )

    class Meta:
        ordering = ["order"]
        verbose_name = "Вопрос теста"
        verbose_name_plural = "Вопросы тестов"


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answer_options")
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.text} ({'Ok' if self.is_correct else 'No'})"


class MatchingItem(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class MatchingAnswerOption(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="matching_options"
    )
    left = models.ForeignKey(MatchingItem, on_delete=models.CASCADE, related_name="left_options")
    right = models.ForeignKey(MatchingItem, on_delete=models.CASCADE, related_name="right_options")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = [["question", "left"]]

    def __str__(self):
        return f"{self.left.text} <-> {self.right.text}"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now=True)
    is_correct = models.BooleanField(default=False)

    class ANSWER_JSON_KEYS:
        SELECTED_KEY = "selected"
        PAIRS_KEY = "pairs"

    answer_data = models.JSONField(default=dict)
    # SINGLE_CHOICE: {"selected": 5} (ID выбранного AnswerOption)
    # MULTIPLE_CHOICE: {"selected": [5, 7, 9]}
    # MATCHING: {"pairs": {"1": "3", "2": "4"}} (left_id → right_id)
    # TEXT_ANSWER: {"text": "Ответ пользователя"}

    class Meta:
        unique_together = [["user", "question"]]  # Один ответ на вопрос от пользователя
        indexes = [
            models.Index(fields=["user", "question"]),
            models.Index(fields=["is_correct"]),
        ]

    def save(self, *args, **kwargs):
        self.is_correct = self.check_correctness()
        super().save(*args, **kwargs)

    def check_correctness(self):
        if self.question.kind == QuestionKind.SINGLE_CHOICE:
            correct_option = self.question.answer_options.filter(is_correct=True).first()
            return correct_option and (
                self.answer_data.get(self.ANSWER_JSON_KEYS.SELECTED_KEY) == correct_option.id
            )

        elif self.question.kind == QuestionKind.MULTIPLE_CHOICE:
            correct_ids = list(
                self.question.answer_options.filter(is_correct=True).values_list("id", flat=True)
            )
            return set(self.answer_data.get(self.ANSWER_JSON_KEYS.SELECTED_KEY, [])) == set(
                correct_ids
            )

        elif self.question.kind == QuestionKind.MATCHING:
            correct_pairs = {
                str(pair.left): str(pair.right) for pair in self.question.matching_options.all()
            }
            return self.answer_data.get(self.ANSWER_JSON_KEYS.PAIRS_KEY, {}) == correct_pairs
        return False
