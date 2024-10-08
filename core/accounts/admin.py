from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_staff", "is_active",)
    list_filter =  ("email", "is_staff", "is_active",)
    search_fields = ('email',)
    ordering = ("email",)

    fieldsets = (
        ('Accoount', {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2", "is_staff", "is_active", "groups", "user_permissions")}),
    )


admin.site.register(User, CustomUserAdmin)