import os
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Fill all apps with test data"

    def handle(self, *args, **options):
        # Последовательность заполнения важна, если есть зависимости между моделями
        apps_to_fill = [
            ("users", {"count": 20, "drop": False}),
            (
                "education",
                {
                    "courses": 10,
                },
            ),
        ]

        for app_name, params in apps_to_fill:
            self.stdout.write(f"Filling {app_name} data...")
            try:
                call_command(f"fill_{app_name}_data", **params)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error filling {app_name}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("Successfully filled all data!"))
