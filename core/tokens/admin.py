# tokens/admin.py

from django.contrib import admin
from .models import Token

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('_id', '_user', 'token', 'is_active', 'expired_at', 'created_at')
    list_filter = ('is_active', 'expired_at', 'created_at')
    search_fields = ('_user__email', 'token')
    readonly_fields = ('_id', 'token', 'created_at', 'updated_at')
