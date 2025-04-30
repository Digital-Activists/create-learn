from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
from tqdm import tqdm

from CreateLearn.apps.users.models import Student, Teacher
from ...models import Course, Lesson

User = get_user_model()
fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Fill education app with test data with users dependencies"

    def add_arguments(self, parser):
        parser.add_argument("--courses", type=int, default=10, help="Number of courses to create")
        parser.add_argument("--drop", type=bool, default=False, help="Drop data before fill")

    def handle(self, *args, **options):
        teachers = Teacher.objects.all()
        students = Student.objects.all()
        lessons_count = 0

        if teachers.count() == 0 or students.count() == 0:
            self.stdout.write(
                self.style.ERROR("No teachers or students found. Please create some first.")
            )
            return

        if options["drop"]:
            Course.objects.all().delete()
            Lesson.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("All courses and lessons deleted."))

        # Создаем курсы
        for i in tqdm(range(options["courses"]), desc="Creating courses"):
            teacher = fake.random_element(teachers)
            (course, created) = Course.objects.get_or_create(
                title=f"Курс по {fake.word().capitalize()}",
                description=fake.text(),
                creator=teacher.user,
                is_published=fake.boolean(85),
            )

            # Добавляем случайных студентов на курс
            course.students.set(
                map(
                    lambda student: student.user,
                    fake.random_elements(students, length=fake.random_int(1, 10)),
                ),
            )

            # Создаем уроки
            for j in range(fake.random_int(2, 10)):
                Lesson.objects.get_or_create(
                    course=course, title=fake.sentence(), order=j, content=fake.text()
                )
                lessons_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Created {options["courses"]} courses with {lessons_count} lessons.'
            )
        )
