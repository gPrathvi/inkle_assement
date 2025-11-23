import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create a Django superuser from env vars if it doesn't already exist."

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv("ADMIN_USERNAME")
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")

        if not username or not password:
            self.stdout.write(self.style.WARNING("ADMIN_USERNAME or ADMIN_PASSWORD not set; skipping admin creation."))
            return

        user, created = User.objects.get_or_create(username=username, defaults={"email": email or ""})
        if created:
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'."))
        else:
            # Ensure the user has superuser/staff flags and update password if provided
            updated = False
            if not user.is_superuser or not user.is_staff:
                user.is_superuser = True
                user.is_staff = True
                updated = True
            if password:
                user.set_password(password)
                updated = True
            if email and user.email != email:
                user.email = email
                updated = True
            if updated:
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Updated superuser '{username}'."))
            else:
                self.stdout.write(self.style.NOTICE(f"Superuser '{username}' already exists and is up to date."))
