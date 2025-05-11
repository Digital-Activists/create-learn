from django.core.management.base import BaseCommand
from faker import Faker
from ...models import Role, Student, Teacher, CustomUser
from tqdm import tqdm


fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Fill users app with test data"
    roles = [Role.TEACHER, Role.STUDENT]

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=20, help="Number of users to create")
        parser.add_argument("--drop", action="store_true", help="Drop data before fill")

    def handle(self, *args, **options):
        if options["drop"]:
            CustomUser.objects.all().delete()
            Teacher.objects.all().delete()
            Student.objects.all().delete()
            self.stdout.write(self.style.WARNING("All Users deleted."))

        admin_created = self.create_admin("admin@admin.com", "admin")

        for _ in tqdm(range(options["count"]), desc="Creating users"):
            role = fake.random_element(elements=self.roles)

            user = CustomUser.objects.create_user(
                email=fake.unique.email(),
                password="testpass123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                middle_name=fake.middle_name(),
                phone=fake.phone_number(),
                date_of_birth=fake.date_of_birth(),
                role=role,
            )
            if role == Role.TEACHER:
                self.create_random_teacher(user)
            elif role == Role.STUDENT:
                self.create_random_student(user)

        self.stdout.write(
            self.style.SUCCESS(
                f'Created {options["count"]} users + {1 if admin_created else 0} admin'
            )
        )

    def create_admin(self, email: str, password: str):
        if not CustomUser.objects.filter(email=email).exists():
            admin = CustomUser.objects.create_superuser(
                email=email,
                password=password,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                middle_name=fake.middle_name(),
                phone=fake.phone_number(),
                date_of_birth=fake.date_of_birth(),
            )
            self.create_random_student(admin)
            self.create_random_teacher(admin)
            return True
        return False

    @staticmethod
    def create_random_teacher(user: CustomUser):
        experience_values = [choice[0] for choice in Teacher.TeachingExperience.choices]

        (teacher, created) = Teacher.objects.get_or_create(
            user=user,
            teaching_experience=fake.random_element(elements=experience_values),
            about_oneself=fake.paragraph(),
            teaching_subjects=fake.job(),
            qualification=fake.job(),
        )
        return teacher

    @staticmethod
    def create_random_student(user: CustomUser):
        course_values = [choice[0] for choice in Student.CourseLevel.choices]
        class_values = [choice[0] for choice in Student.ClassLevel.choices]

        (student, created) = Student.objects.get_or_create(
            user=user,
            educational_institution=fake.company(),
            course=fake.random_element(elements=course_values),
            class_level=fake.random_element(elements=class_values),
        )
        return student
