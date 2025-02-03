from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from . import choices
class User(AbstractUser):
    email = models.EmailField(_("Email"), unique=True, null=False)
    user_status = models.CharField(max_length=100, blank=True,null=True,choices=choices.UserStatus.choices)
    name = models.CharField(max_length=100, blank=True,null=True)
    permissions = models.CharField(max_length=150,null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    

    def __str__(self):
        return self.email