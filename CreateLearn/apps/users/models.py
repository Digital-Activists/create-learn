from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


class Role(models.TextChoices):
    TEACHER = "TEACHER", "Учитель"
    STUDENT = "STUDENT", "Студент"
    ADMIN = "ADMIN", "Администратор"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "ADMIN")  # Или другая роль по умолчанию

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    # Убираем username и делаем email уникальным идентификатором
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    middle_name = models.CharField(max_length=150, verbose_name="Отчество", blank=True)
    date_of_birth = models.DateField(verbose_name="Дата рождения", null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Аватар")
    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.STUDENT, verbose_name="Роль"
    )

    USERNAME_FIELD = "email"  # Указываем, что email — поле для входа
    REQUIRED_FIELDS = []  # Убираем username из обязательных полей

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"


class Student(models.Model):
    class CourseLevel(models.TextChoices):
        YEAR_1_2 = "1-2", "1-2 курс(бакалавриат/специалитет)"
        YEAR_3_4 = "3-4", "3-4 курс(бакалавриат/специалитет)"
        YEAR_5_6 = "5-6", "5-6 курс(специалитет)"
        MASTER = "MASTER", "магистратура(любой курс)"

    class ClassLevel(models.TextChoices):
        CLASS_5_6 = "5-6", "5-6 класс"
        CLASS_7_9 = "7-9", "7-9 класс"
        CLASS_10_11 = "10-11", "10-11 класс"

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student")
    educational_institution = models.CharField(
        max_length=100, verbose_name="Учебное заведение", blank=True
    )
    course = models.CharField(
        max_length=10, choices=CourseLevel.choices, blank=True, verbose_name="Курс"
    )
    class_level = models.CharField(
        max_length=5, choices=ClassLevel.choices, blank=True, verbose_name="Класс"
    )


class Teacher(models.Model):
    class TeachingExperience(models.TextChoices):
        LESS_1_YEAR = "0-1", "менее 1 года"
        YEAR_1_2 = "1-2", "1-2 года"
        YEARS_3_4 = "3-4", "3-4 лет"
        YEARS_5_7 = "5-7", "5-7 лет"
        YEARS_8_10 = "8-10", "8-10 лет"
        OVER_10 = "10+", "более 10 лет"

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="teacher")
    teaching_experience = models.CharField(
        max_length=5,
        choices=TeachingExperience.choices,
        default=TeachingExperience.LESS_1_YEAR,
        verbose_name="Опыт преподавания",
    )
    about_oneself = models.TextField(verbose_name="О себе", blank=True)
    teaching_subjects = models.CharField(
        max_length=100, verbose_name="Преподаваемые предметы", blank=True
    )
    qualification = models.CharField(
        max_length=100, verbose_name="Квалификация/Образование", blank=True
    )
