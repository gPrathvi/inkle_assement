from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from posts.models import Post

class Command(BaseCommand):
    help = "Seed demo data: ensures an admin user exists and creates a sample post if none exists."

    def handle(self, *args, **options):
        User = get_user_model()
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            self.stdout.write(self.style.WARNING("No superuser found. Run create_admin_if_needed first or create one manually."))
            return
        if not Post.objects.exists():
            Post.objects.create(author=admin, content="Welcome to Inkle! This is a demo post.")
            self.stdout.write(self.style.SUCCESS("Created a demo post."))
        else:
            self.stdout.write(self.style.NOTICE("Posts already exist; skipping demo data."))
