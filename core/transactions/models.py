from django.db import models
import uuid
from django.contrib.auth import get_user_model
from core.utils.basemodel import Model


User = get_user_model()

class TransactionCategory(Model):
    """
    Model for transaction categories.
    This model uses a tree structure to create nested categories.
    parent: To create a relationship between categories, where a category can be a child of another.
    """
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    CATEGORY_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES, default='expense')


    def __str__(self):
        return self.name

class Transaction(Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    _user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    _category = models.ForeignKey(TransactionCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    description = models.TextField()
    tag = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self._id} - {self._user}'
