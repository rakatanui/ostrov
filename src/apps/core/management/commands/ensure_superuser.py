import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or update a superuser from explicit arguments or environment variables."

    def add_arguments(self, parser):
        parser.add_argument("--username", default=os.getenv("DJANGO_SUPERUSER_USERNAME"))
        parser.add_argument("--email", default=os.getenv("DJANGO_SUPERUSER_EMAIL", ""))
        parser.add_argument("--password", default=os.getenv("DJANGO_SUPERUSER_PASSWORD"))
        parser.add_argument(
            "--skip-if-missing",
            action="store_true",
            help="Exit successfully if required values are not provided.",
        )

    def handle(self, *args, **options):
        username = (options["username"] or "").strip()
        email = (options["email"] or "").strip()
        password = options["password"]

        if not username or not password:
            if options["skip_if_missing"]:
                self.stdout.write(
                    self.style.WARNING(
                        "Skipping superuser creation because username or password is missing."
                    )
                )
                return
            raise CommandError(
                "Superuser credentials are incomplete. Provide --username and --password "
                "or set DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD."
            )

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        fields_to_update = []
        if email and getattr(user, "email", "") != email:
            user.email = email
            fields_to_update.append("email")
        if not user.is_staff:
            user.is_staff = True
            fields_to_update.append("is_staff")
        if not user.is_superuser:
            user.is_superuser = True
            fields_to_update.append("is_superuser")

        user.set_password(password)
        fields_to_update.append("password")

        if created:
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'."))
            return

        user.save(update_fields=fields_to_update)
        self.stdout.write(self.style.SUCCESS(f"Updated superuser '{username}'."))
