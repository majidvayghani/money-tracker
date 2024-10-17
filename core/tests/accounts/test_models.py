from django.test import TestCase
from django.db.utils import IntegrityError
from accounts.models import User
import pytest



# ToDo: create test for profile model

class UserModelTest(TestCase):
    @pytest.mark.unit
    def setUp(self):
        # Set up a sample user for testing
        self.email = "test@example.com"
        self.user = User.objects.create(
            email=self.email,
            is_staff=False,
            is_active=True
        )

    @pytest.mark.unit
    def test_create_user(self):
        """Test if a user is created successfully"""
        self.assertEqual(self.user.email, self.email)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertIsNotNone(self.user._id)  # Check if UUID is generated
    
    @pytest.mark.unit
    def test_user_str(self):
        """Test the string representation of the user"""
        self.assertEqual(str(self.user), self.email)

    @pytest.mark.unit
    def test_get_user_by_email(self):
        """Test retrieving a user by email"""
        user = User.get_user_by_email(self.email)
        self.assertEqual(user, self.user)

    @pytest.mark.unit
    def test_get_user_by_email_nonexistent(self):
        """Test retrieving a non-existent user by email"""
        user = User.get_user_by_email("nonexistent@example.com")
        self.assertIsNone(user)

    @pytest.mark.unit
    def test_get_user_id_by_email(self):
        """Test retrieving user ID by email"""
        _id = User.get_user_id_by_email(self.email)
        self.assertEqual(_id, self.user._id)
    
    @pytest.mark.unit
    def test_get_user_id_by_email_nonexistent(self):
        """Test retrieving user ID for a non-existent email"""
        user_id = User.get_user_id_by_email("nonexistent@example.com")
        self.assertIsNone(user_id)

    @pytest.mark.unit
    def test_unique_email_constraint(self):
        """Test that creating a user with an existing email raises an IntegrityError"""
        with self.assertRaises(IntegrityError):
            User.objects.create(
                email=self.email,
                is_staff=False,
                is_active=True
            )
