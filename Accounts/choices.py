from django.db import models
class UserStatus(models.TextChoices):
    ADMIN = "admin", "Admin"
    SIMPLE_USER = "simple_user", "Simple User"