from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", '_id', "is_staff", "is_active",)
    list_filter =  ("email", "is_staff", "is_active",)
    search_fields = ('email',)
    ordering = ("email",)

    fieldsets = (
        ('Accoount', {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {"fields": ("email", "password2", "is_staff", "is_active", "groups", "user_permissions")}),
    )


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['_id', '_user', 'first_name', 'last_name']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
