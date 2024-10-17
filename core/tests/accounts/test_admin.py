from django.test import TestCase
from django.contrib.admin.sites import site
from django.contrib.auth.admin import UserAdmin

from accounts.models import User
from accounts.admin import CustomUserAdmin

class CustomUserAdminTest(TestCase):

    def test_custom_user_admin_registration(self):
        # Check if the CustomUserAdmin is registered for the User model
        self.assertIn(User, site._registry)
        self.assertIsInstance(site._registry[User], CustomUserAdmin)

    def test_custom_user_admin_attributes(self):
        # Ensure the CustomUserAdmin uses the correct model
        admin_instance = site._registry[User]
        self.assertEqual(admin_instance.model, User)

        # Check if list_display is correct
        self.assertEqual(admin_instance.list_display, ("email", '_id', "is_staff", "is_active",))

        # Check if list_filter is correct
        self.assertEqual(admin_instance.list_filter, ("email", "is_staff", "is_active",))

        # Check if search_fields is correct
        self.assertEqual(admin_instance.search_fields, ('email',))

        # Check if ordering is correct
        self.assertEqual(admin_instance.ordering, ("email",))

        # Check if fieldsets are set correctly
        expected_fieldsets = (
            ('Accounts', {"fields": ("email", "password")}),
            ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        )
        self.assertEqual(admin_instance.fieldsets, expected_fieldsets)

        # Check if add_fieldsets are set correctly
        expected_add_fieldsets = (
            (None, {"fields": ("email", "password2", "is_staff", "is_active", "groups", "user_permissions")}),
        )
        self.assertEqual(admin_instance.add_fieldsets, expected_add_fieldsets)
