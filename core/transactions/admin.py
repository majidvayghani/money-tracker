from django.contrib import admin
from .models import Transaction, TransactionCategory

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['amount', '_category', 'description', '_id', '_user']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_income', 'is_expense', '_id']

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionCategory, CategoryAdmin)
