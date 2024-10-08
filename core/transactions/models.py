from django.db import models
import uuid

from core.utils.basemodel import Model
from accounts.models import User

class Transaction(Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    _user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    description = models.TextField()
    tag = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.category} - {self.amount}'
