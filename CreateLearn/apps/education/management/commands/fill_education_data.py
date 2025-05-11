from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
from tqdm import tqdm
import os
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile

from CreateLearn.apps.users.models import Student, Teacher
from ...models import Course, Lesson

User = get_user_model()
fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Fill education app with test data with users dependencies"

    def add_arguments(self, parser):
        parser.add_argument("--courses", type=int, default=10, help="Number of courses to create")
        parser.add_argument("--drop", action="store_true", help="Drop data before fill")

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
            course_title = f"Курс по {fake.word().capitalize()}"
            course = Course(
                title=course_title,
                description=fake.text(),
                creator=teacher.user,
                is_published=fake.boolean(85),
            )

            # Generate and set the avatar
            avatar_image = generate_course_avatar(course_title)
            course.avatar.save(avatar_image.name, avatar_image, save=False)
            course.save()

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


def generate_course_avatar(course_title):
    """
    Generate a simple avatar image for a course with the course title.

    Args:
        course_title (str): The title of the course

    Returns:
        ContentFile: A Django ContentFile containing the image data
    """
    # Define image size and colors
    width, height = 400, 400
    bg_colors = [
        (255, 99, 71),  # Tomato
        (255, 165, 0),  # Orange
        (255, 215, 0),  # Gold
        (154, 205, 50),  # Yellow Green
        (0, 128, 128),  # Teal
        (100, 149, 237),  # Cornflower Blue
        (138, 43, 226),  # Blue Violet
        (255, 105, 180),  # Hot Pink
    ]

    # Create a new image with a random background color
    bg_color = random.choice(bg_colors)
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # Extract the main subject from the course title (after "Курс по ")
    if "Курс по " in course_title:
        main_subject = course_title.split("Курс по ")[1]
    else:
        main_subject = course_title

    # Try to use a font, fall back to default if not available
    try:
        # Try to find a system font
        font_size = 60  # Smaller font size to fit longer text
        font = ImageFont.truetype("Arial", font_size)
    except IOError:
        # If font not found, use default
        font = ImageFont.load_default()
        font_size = 40

    # Handle text positioning and wrapping
    words = main_subject.split()
    lines = []
    current_line = ""

    # Simple text wrapping
    for word in words:
        test_line = current_line + " " + word if current_line else word
        # Check if adding this word would make the line too long
        text_width = (
            draw.textlength(test_line, font=font)
            if hasattr(draw, "textlength")
            else font_size * len(test_line) * 0.6
        )

        if text_width < width - 40:  # Leave some margin
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    # If no lines were created (e.g., single short word), use the main subject directly
    if not lines:
        lines = [main_subject]

    # Calculate total text height
    line_height = font_size * 1.2
    total_height = len(lines) * line_height

    # Starting Y position to center all lines vertically
    y_position = (height - total_height) // 2

    # Draw each line centered horizontally
    for line in lines:
        text_width = (
            draw.textlength(line, font=font)
            if hasattr(draw, "textlength")
            else font_size * len(line) * 0.6
        )
        x_position = (width - text_width) // 2
        draw.text((x_position, y_position), line, fill=(255, 255, 255), font=font)
        y_position += line_height

    # Save the image to a BytesIO object
    image_io = BytesIO()
    image.save(image_io, format="PNG")
    image_io.seek(0)

    # Return a ContentFile that can be assigned to an ImageField
    return ContentFile(
        image_io.getvalue(), name=f"course_avatar_{course_title.replace(' ', '_')[:20]}.png"
    )
