import uuid
from django.db import models
from django.conf import settings
from core.utils.basemodel import Model

class AccessToken(Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    _user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='custom_tokens')
    token = models.CharField(max_length=64, unique=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self._user.email} - {self.token}'
