from django.test import TestCase
from django.db.utils import IntegrityError
from ..models import User

class UserModelTest(TestCase):
    def setUp(self):
        # Set up a sample user for testing
        self.email = "test@example.com"
        self.first_name = "Test"
        self.last_name = "User"
        self.user = User.objects.create(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            is_staff=False,
            is_active=True
        )

    def test_create_user(self):
        """Test if a user is created successfully"""
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.first_name, self.first_name)
        self.assertEqual(self.user.last_name, self.last_name)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertIsNotNone(self.user._id)  # Check if UUID is generated

    def test_user_str(self):
        """Test the string representation of the user"""
        self.assertEqual(str(self.user), self.email)

    def test_get_user_by_email(self):
        """Test retrieving a user by email"""
        user = User.get_user_by_email(self.email)
        self.assertEqual(user, self.user)

    def test_get_user_by_email_nonexistent(self):
        """Test retrieving a non-existent user by email"""
        user = User.get_user_by_email("nonexistent@example.com")
        self.assertIsNone(user)

    def test_get_user_id_by_email(self):
        """Test retrieving user ID by email"""
        _id = User.get_user_id_by_email(self.email)
        self.assertEqual(_id, self.user._id)

    def test_get_user_id_by_email_nonexistent(self):
        """Test retrieving user ID for a non-existent email"""
        user_id = User.get_user_id_by_email("nonexistent@example.com")
        self.assertIsNone(user_id)

    def test_unique_email_constraint(self):
        """Test that creating a user with an existing email raises an IntegrityError"""
        with self.assertRaises(IntegrityError):
            User.objects.create(
                email=self.email,
                first_name="Another",
                last_name="User",
                is_staff=False,
                is_active=True
            )
