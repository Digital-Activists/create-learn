from django.contrib import admin
from .models import (
    Course,
    Lesson,
    Quiz,
    Question,
    AnswerOption,
    MatchingItem,
    MatchingAnswerOption,
    UserAnswer,
    UserProgressLesson,
    UserProgressCourse,
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(MatchingItem)
class MatchingItemAdmin(admin.ModelAdmin):
    pass


@admin.register(MatchingAnswerOption)
class MatchingAnswerOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProgressLesson)
class UserProgressLessonAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProgressCourse)
class UserProgressCourseAdmin(admin.ModelAdmin):
    pass
