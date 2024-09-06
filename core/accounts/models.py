from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

 
from .managers import CustomUserManager


class CustomUser (AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email