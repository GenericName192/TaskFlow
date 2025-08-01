from django.test import TestCase, Client
from .models import User
from django.db import IntegrityError
from django.urls import reverse
from task.models import Task


class BaseAuthUserTest(TestCase):
    """Base class with a common setUp"""
    def setUp(self):
        """ Sets things up before each test """
        self.test_user = User.objects.create(
            username="Test_account",
            first_name="Testy",
            last_name="Mc-Test",
            email="test_email@test.com",
            boss=None
        )
        self.test_user2 = User.objects.create(
            username="Test_account2",
            first_name="Testy",
            last_name="Mc-Test The Second",
            email="test_email2@test.com",
            boss=self.test_user
        )
        self.test_user3 = User.objects.create(
            username="Test_account3",
            first_name="Testy",
            last_name="Mc-Test The Third",
            email="test_email3@test.com",
            password="Placeholder123",
            boss=self.test_user2
        )
        self.test_user.set_password("Placeholder123")
        self.test_user.save()


class AuthUserModelTest(BaseAuthUserTest):
    """Test cases for the User model"""

    # Test user creation with all required fields
    def test_User_model_creation(self):
        test_user4 = User.objects.create(
            username="Test_account4",
            first_name="Testy",
            last_name="Mc-Test The Fourth",
            email="test_email4@test.com",
            password="Placeholder123",
            boss=None
        )
        self.assertTrue(isinstance(test_user4, User))
        self.assertEqual(User.objects.count(), 4)

    # Test full_name property returns correct formatted name (first + last)
    def test_full_name(self):
        self.assertEqual(self.test_user.full_name, "Testy Mc-Test")

    # Test __str__ method returns username
    def test_string(self):
        self.assertEqual(str(self.test_user), "Test_account")

    # Test email uniqueness constraint
    def test_email_unique(self):
        with self.assertRaises(IntegrityError):
            self.test_user = User.objects.create(
                username="Test_account",
                first_name="Testy",
                last_name="Mc-Test",
                email="test_email@test.com",
                password="Placeholder123",
                boss=None
            )

    # Test default values for first_name and last_name
    def test_defaults(self):
        test_user = User.objects.create(
            username="Testy",
            email="Testy@test.test",
            password="Placeholder123"
        )
        self.assertEqual(test_user.first_name, "test")
        self.assertEqual(test_user.last_name, "test")

    # Test get_direct_subordinates() returns correct users
    def test_direct_subordinates(self):
        self.assertEqual(list(self.test_user.get_direct_subordinates()),
                         [self.test_user2])

    # Test get_all_subordinates() traverses hierarchy correctly
    def test_all_subordinates(self):
        self.assertEqual(list(self.test_user.get_all_subordinates()),
                         [self.test_user2, self.test_user3])

    # Test boss-subordinate relationship (ForeignKey works properly)
    def test_boss_subordinate(self):
        self.assertEqual(self.test_user2.boss, self.test_user)
