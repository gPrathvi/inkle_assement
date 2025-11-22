from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'
    ROLE_OWNER = 'owner'
    ROLE_CHOICES = [
        (ROLE_USER, 'User'),
        (ROLE_ADMIN, 'Admin'),
        (ROLE_OWNER, 'Owner'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)

    def is_admin(self):
        return self.role in {self.ROLE_ADMIN, self.ROLE_OWNER}

    def is_owner(self):
        return self.role == self.ROLE_OWNER

# Create your models here.
