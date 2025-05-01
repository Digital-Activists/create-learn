from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from unidecode import unidecode

User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса")
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    description = models.TextField(blank=True, verbose_name="Описание курса")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_courses")
    students = models.ManyToManyField(User, related_name="enrolled_courses", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    avatar = models.ImageField(
        upload_to="course_avatars/", verbose_name="Аватар", blank=True, null=True
    )

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("course_details", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            creator_slug = slugify(unidecode(str(self.creator)))
            title_slug = slugify(unidecode(self.title))

            if not creator_slug or not title_slug:
                raise ValueError(
                    f"creator_slug: {creator_slug} and title_slug: {title_slug} must contain valid characters to generate a slug."
                )

            self.slug = f"{title_slug}-{creator_slug}"
        return super().save(*args, **kwargs)


class UserProgressCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
