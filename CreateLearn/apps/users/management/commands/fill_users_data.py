from django.core.management.base import BaseCommand
from faker import Faker
from ...models import Role, Student, Teacher, CustomUser


fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Fill users app with test data"
    roles = [r[0] for r in (Role.TEACHER, Role.STUDENT)]

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=20, help="Number of users to create")
        parser.add_argument("--drop", type=bool, default=False, help="Drop data before fill")

    def handle(self, *args, **options):
        if options["drop"]:
            CustomUser.objects.all().delete()
            Teacher.objects.all().delete()
            Student.objects.all().delete()
            self.stdout.write(self.style.WARNING("All Users deleted."))

        admin_created = self.create_admin("admin@admin.com", "admin")

        for _ in range(options["count"]):
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
            if role == Role.TEACHER[0]:
                Teacher.objects.get_or_create(
                    user=user,
                    teaching_experience=fake.random_element(
                        elements=Teacher.TeachingExperience.choices
                    ),
                    about_oneself=fake.paragraph(),
                    teaching_subjects=fake.job(),
                    qualification=fake.job(),
                )
            elif role == Role.STUDENT[0]:
                Student.objects.get_or_create(
                    user=user,
                    educational_institution=fake.company(),
                    course=fake.random_element(elements=Student.CourseLevel.choices),
                    class_level=fake.random_element(elements=Student.ClassLevel.choices),
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Created {options["count"]} users + {1 if admin_created else 0} admin'
            )
        )

    def create_admin(self, email: str, password: str):
        if CustomUser.objects.filter(email=email).count == 0:
            CustomUser.objects.create_superuser(email=email, password=password)
            return True
        return False
