from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import uuid

from core.utils.basemodel import Model
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
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

    @classmethod
    def get_user_id_by_email(cls, email):
        user = cls.get_user_by_email(email)
        if user:
            return user._id
        return None
    
    @classmethod
    def get_profile_by_email(cls, email):
        user = cls.get_user_id_by_email(email)
        if user:
            return Profile.user
        return None


class Profile(Model):
    """
        Advantages:
        - Separation of Concerns: Keeps authentication-related fields separate from user profile information.
        - Flexibility: Allows adding or modifying profile fields without altering the User model.
        - Scalability: Facilitates easier management and scaling of user-related data.
    """
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    _user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=125, null=False, default='first_name')
    last_name = models.CharField(max_length=125, null=False, default='last_name')

    def __str__(self):
        return self._user.email
