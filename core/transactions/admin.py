from django.contrib import admin
from .models import Transaction

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['amount', 'category', 'description', '_id', '_user']

admin.site.register(Transaction, TransactionAdmin)
