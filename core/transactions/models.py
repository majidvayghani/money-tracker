from django.db import models
import uuid

from core.utils.basemodel import Model
from accounts.models import Profile

class Transaction(Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    _profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    description = models.TextField()
    tag = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self._id} - {self._profile}'
