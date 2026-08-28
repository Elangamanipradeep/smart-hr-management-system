import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Create or update the production admin user"

    def handle(self, *args, **options):

        User = get_user_model()

        username = os.environ.get("ADMIN_USERNAME", "admin")
        email = os.environ.get(
            "ADMIN_EMAIL",
            "admin@example.com"
        )
        password = os.environ.get("ADMIN_PASSWORD")

        if not password:
            self.stdout.write(
                self.style.ERROR(
                    "ADMIN_PASSWORD environment variable is not set."
                )
            )
            return

        # Get or create Admin group
        admin_group, created = Group.objects.get_or_create(
            name="Admin"
        )

        # Get or create admin user
        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        # Make sure admin account has correct properties
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.email = email

        # Set password
        user.set_password(password)

        user.save()

        # Add Admin group
        user.groups.add(admin_group)

        if user_created:

            self.stdout.write(
                self.style.SUCCESS(
                    f"Superuser '{username}' created successfully."
                )
            )

        else:

            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin user '{username}' updated successfully."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"User '{username}' added to Admin group."
            )
        )