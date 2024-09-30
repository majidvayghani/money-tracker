from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
import uuid

from core.utils.basemodel import Model
from .managers import UserManager


class User (AbstractBaseUser, PermissionsMixin, Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=125, null=False)
    last_name = models.CharField(max_length=125, null=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
    @classmethod
    def get_user_by_email(cls, email):
        try:
            user = cls.objects.get(email=email)
            return user
        except cls.DoesNotExist:
            return None