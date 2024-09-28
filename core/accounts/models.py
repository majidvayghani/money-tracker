from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
import uuid

from .managers import UserManager


class User (AbstractBaseUser, PermissionsMixin):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email