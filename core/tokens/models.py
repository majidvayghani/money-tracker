import uuid
import secrets
from django.db import models
from django.conf import settings
from core.utils.basemodel import Model
from django.utils import timezone
from datetime import timedelta

class Token(Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    _user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tokens'
    )
    is_active = models.BooleanField(default=True)
    token = models.CharField(max_length=255, unique=True, editable=False)
    expired_at = models.DateTimeField()

    def __str__(self):
        return f'{self._user.email} - {self.token}'

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)
        if not self.expired_at:
            self.expired_at = timezone.now() + timedelta(hours=1)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expired_at
