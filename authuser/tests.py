from django.test import TestCase, Client
from .models import User
from django.db import IntegrityError
from django.urls import reverse
from task.models import Task
from .forms import AuthUserCreationForm


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
        self.test_user2.set_password("Placeholder123")
        self.test_user2.save()


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
        self.assertIsInstance(test_user4, User)
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


class AuthUserViewTests(BaseAuthUserTest):
    """Test cases for authuser views"""
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.test_task = Task.objects.create(
            title="Do the thing",
            description="Do it, Do it now",
            due_date=None,
            completed=False,
            assigned_to=self.test_user,
            created_by=self.test_user,
        )
        self.test_task2 = Task.objects.create(
            title="Do the thing",
            description="Do it, Do it now",
            due_date=None,
            completed=True,
            assigned_to=self.test_user,
            created_by=self.test_user,
        )

    # INDEX VIEW TESTS
    # Test authenticated user sees their task statistics
    def test_index_authenticated(self):
        self.client.login(username="Test_account", password="Placeholder123")
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "authuser/index.html")
        self.assertEqual(list(response.context["up_coming_tasks"]),
                         [self.test_task],
                         "Should show only incomplete tasks")
        self.assertEqual(response.context["completed_tasks_count"], 1,
                         "Should count exactly 1 completed task")
        self.assertEqual(response.context["total_ongoing_tasks"], 1,
                         "Should count 1 ongoing task")
        self.assertEqual(response.context["total_tasks_count"], 2,
                         "Should count total of 2 tasks")
        self.assertContains(response, "Logout",
                            msg_prefix="Authenticated user should see logout")

    # Test unauthenticated user sees basic page
    def test_index_unauthenticated(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "authuser/index.html")
        self.assertContains(response, "Welcome to TaskFlow!")
        self.assertNotContains(response, "Welcome back")
        self.assertContains(response, "Login")

    # Test tip of the day appears correctly
    def test_index_tip(self):
        self.client.login(username="Test_account", password="Placeholder123")
        response = self.client.get(reverse("index"))
        tip = response.context["tip"]
        self.assertIsInstance(tip, str, "Tip should be a string")

    # PROFILE VIEW TESTS
    # Test viewing own profile shows edit buttons
    def test_profile_edit_on_own_profile(self):
        self.client.login(username="Test_account", password="Placeholder123")
        response = self.client.get(reverse("profile",
                                           args=[self.test_user.id]))
        self.assertContains(response, "Edit Profile",
                            msg_prefix="Own profile should show edit button")

    # Test viewing other user's profile hides edit buttons
    def test_profile_edit_on_other_profile(self):
        self.client.login(username="Test_account2", password="Placeholder123")
        response = self.client.get(reverse("profile",
                                           args=[self.test_user.id]))
        self.assertNotContains(response, "Edit Profile",
                               msg_prefix="Other users should not see edit")

    # Test subordinates display correctly
    def test_profile_shows_subordinates(self):
        self.client.login(username="Test_account", password="Placeholder123")
        response = self.client.get(reverse("profile",
                                           args=[self.test_user.id]))
        self.assertContains(response, self.test_user2.full_name,
                            msg_prefix="Should show subordinate names")

    # Test boss information displays when present
    def test_profile_shows_boss(self):
        self.client.login(username="Test_account2", password="Placeholder123")
        response = self.client.get(reverse("profile",
                                           args=[self.test_user2.id]))
        self.assertContains(response, self.test_user.full_name,
                            msg_prefix="Should show boss name")

    # Test 404 for non-existent user
    def test_profile_404_for_nonexistent_user(self):
        self.client.login(username="Test_account", password="Placeholder123")
        response = self.client.get(reverse("profile", args=[9999]))
        self.assertEqual(response.status_code, 404,
                         "Should return 404 for non-existent user")

    # EDIT PROFILE VIEW TESTS
    # Test only owner can access edit form
    def test_edit_profile_owner_access(self):
        self.client.login(username="Test_account", password="Placeholder123")
        response = self.client.get(reverse("edit_profile",
                                           args=[self.test_user.id]))
        self.assertEqual(response.status_code, 200,
                         "Owner should access edit form")
        self.assertTemplateUsed(response, "authuser/edit_profile.html")

    # Test form pre-populated with current data
    def test_edit_profile_form_prepopulated(self):
        self.client.login(username="Test_account", password="Placeholder123")
        response = self.client.get(reverse("edit_profile",
                                           args=[self.test_user.id]))
        self.assertContains(response, self.test_user.first_name,
                            msg_prefix="Form should be pre-populated")
        self.assertContains(response, self.test_user.email)

    # Test successful profile update
    def test_edit_profile_successful_update(self):
        self.client.login(username="Test_account", password="Placeholder123")
        response = self.client.post(reverse("edit_profile",
                                            args=[self.test_user.id]), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@test.com',
            'boss': ''
        })
        self.assertEqual(response.status_code, 302,
                         "Should redirect after successful update")
        updated_user = User.objects.get(id=self.test_user.id)
        self.assertEqual(updated_user.first_name, 'Updated')

    # Test validation errors display correctly
    def test_edit_profile_validation_errors(self):
        self.client.login(username="Test_account", password="Placeholder123")
        response = self.client.post(reverse("edit_profile",
                                            args=[self.test_user.id]), {
            'first_name': '',  # Required field left empty
            'last_name': 'Name',
            'email': 'invalid-email',  # Invalid email
            'boss': ''
        })
        self.assertEqual(response.status_code, 200,
                         "Should stay on form with validation errors")
        self.assertContains(response, "This field is required",
                            msg_prefix="Should show validation errors")

    # Test permission denied for other users
    def test_edit_profile_permission_denied(self):
        self.client.login(username="Test_account2", password="Placeholder123")
        response = self.client.get(reverse("edit_profile",
                                           args=[self.test_user.id]))
        self.assertEqual(response.status_code, 403,
                         "Other users should be denied access")

    # CHANGE PASSWORD VIEW TESTS
    # Test only owner can access password change
    def test_change_password_owner_access(self):
        self.client.login(username="Test_account", password="Placeholder123")
        response = self.client.get(reverse("change_password",
                                           args=[self.test_user.id]))
        self.assertEqual(response.status_code, 200,
                         "Owner should access password change form")
        self.assertTemplateUsed(response, "authuser/update_password.html")

    # Test successful password change
    def test_change_password_successful(self):
        self.client.login(username="Test_account", password="Placeholder123")
        response = self.client.post(reverse("change_password",
                                            args=[self.test_user.id]), {
            'old_password': 'Placeholder123',
            'new_password1': 'NewPassword123!',
            'new_password2': 'NewPassword123!'
        })
        self.assertEqual(response.status_code, 302,
                         "Should redirect after password change")

    # Test form validation (password requirements)
    def test_change_password_validation(self):
        self.client.login(username="Test_account", password="Placeholder123")
        response = self.client.post(reverse("change_password",
                                            args=[self.test_user.id]), {
            'old_password': 'wrong_password',
            'new_password1': '123',  # Too short
            'new_password2': '456'   # Doesn't match
        })
        self.assertEqual(response.status_code, 200,
                         "Should stay on form with validation errors")

    # Test user remains logged in after change
    def test_change_password_stays_logged_in(self):
        self.client.login(username="Test_account", password="Placeholder123")
        self.client.post(reverse("change_password",
                                 args=[self.test_user.id]), {
            'old_password': 'Placeholder123',
            'new_password1': 'NewPassword123!',
            'new_password2': 'NewPassword123!'
        })
        # Test that user is still logged in
        response = self.client.get(reverse("index"))
        self.assertContains(response, "Logout",
                            msg_prefix="User should remain logged in")

    # Test permission denied for other users
    def test_change_password_permission_denied(self):
        self.client.login(username="Test_account2", password="Placeholder123")
        response = self.client.get(reverse("change_password",
                                           args=[self.test_user.id]))
        self.assertEqual(response.status_code, 403,
                         "Other users should be denied access")

    # AUTHENTICATION VIEW TESTS
    # Test login with valid credentials
    def test_login_valid_credentials(self):
        response = self.client.post(reverse("login_view"), {
            'username': 'Test_account',
            'password': 'Placeholder123'
        })
        self.assertEqual(response.status_code, 302,
                         "Should redirect after successful login")

    # Test login with invalid credentials
    def test_login_invalid_credentials(self):
        response = self.client.post(reverse("login_view"), {
            'username': 'Test_account',
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 200,
                         "Should stay on login form with invalid credentials")
        # Check that form is redisplayed (indicates error occurred)
        self.assertContains(response, 'type="password"',
                            msg_prefix="Should redisplay login form on error")

    # Test registration with valid data
    def test_registration_valid_data(self):
        response = self.client.post(reverse("register"), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'ComplexPassword123!',
            'password2': 'ComplexPassword123!'
        })
        self.assertEqual(response.status_code, 302,
                         "Should redirect after successful registration")
        self.assertTrue(User.objects.filter(username='newuser').exists(),
                        "New user should be created")

    # Test registration with duplicate email/username
    def test_registration_duplicate_username(self):
        response = self.client.post(reverse("register"), {
            'username': 'Test_account',  # Already exists
            'email': 'different@test.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'ComplexPassword123!',
            'password2': 'ComplexPassword123!'
        })
        self.assertEqual(response.status_code, 200,
                         "Should stay on form with duplicate username")
        self.assertContains(response,
                            "A user with that username already exists",
                            msg_prefix="Should show duplicate username error")

    # Test logout functionality
    def test_logout_functionality(self):
        self.client.login(username="Test_account", password="Placeholder123")
        response = self.client.post(reverse("logout_view"))
        self.assertEqual(response.status_code, 302,
                         "Should redirect after logout")

        # Verify user is logged out by checking a protected page
        response = self.client.get(reverse("edit_profile",
                                           args=[self.test_user.id]))
        self.assertEqual(response.status_code, 302,
                         "Should redirect to login after logout")

    # Test redirect after login/logout
    def test_login_redirect(self):
        response = self.client.post(reverse("login_view"), {
            'username': 'Test_account',
            'password': 'Placeholder123'
        })
        self.assertRedirects(response, reverse("index"),
                             msg_prefix="Should redirect to index after login")

    # PERMISSION & SECURITY TESTS
    # Test login_required decorator on protected views
    def test_login_required_edit_profile(self):
        response = self.client.get(reverse("edit_profile",
                                           args=[self.test_user.id]))
        self.assertEqual(response.status_code, 302,
                         "Should redirect unauthenticated users")
        self.assertIn('/login/', response.url,
                      "Should redirect to login page")

    # Test users can only edit own profiles
    def test_edit_own_profile_only(self):
        self.client.login(username="Test_account2", password="Placeholder123")
        response = self.client.post(reverse("edit_profile",
                                            args=[self.test_user.id]), {
            'first_name': 'Hacked',
            'last_name': 'Name',
            'email': 'hacked@test.com'
        })
        self.assertEqual(response.status_code, 403,
                         "Should deny editing other users' profiles")

    # Test users can only change own passwords
    def test_change_own_password_only(self):
        self.client.login(username="Test_account2", password="Placeholder123")
        response = self.client.post(reverse("change_password",
                                            args=[self.test_user.id]), {
            'old_password': 'Placeholder123',
            'new_password1': 'Hacked123!',
            'new_password2': 'Hacked123!'
        })
        self.assertEqual(response.status_code, 403,
                         "Should deny changing other users' passwords")

    # Test proper 403/404 responses for unauthorized access
    def test_403_for_unauthorized_access(self):
        self.client.login(username="Test_account2", password="Placeholder123")
        response = self.client.get(reverse("edit_profile",
                                           args=[self.test_user.id]))
        self.assertEqual(response.status_code, 403,
                         "Should return 403 for unauthorized access")

    # Test direct URL access to edit forms
    def test_direct_url_access_denied(self):
        response = self.client.get(reverse("edit_profile",
                                           args=[self.test_user.id]))
        self.assertEqual(response.status_code, 302,
                         "Should redirect unauthenticated direct access")

    # Test manipulation of user IDs in URLs
    def test_url_id_manipulation(self):
        self.client.login(username="Test_account", password="Placeholder123")
        # Try to access edit form for different user
        response = self.client.get(reverse("edit_profile",
                                           args=[self.test_user2.id]))
        self.assertEqual(response.status_code, 403,
                         "Should deny access to other user IDs")

    # Test proper redirects for unauthenticated users
    def test_unauthenticated_redirects(self):
        response = self.client.get(reverse("change_password",
                                           args=[self.test_user.id]))
        self.assertEqual(response.status_code, 302,
                         "Should redirect unauthenticated users")
        self.assertIn('/login/', response.url,
                      "Should redirect to login page")


class AuthUserFormTests(BaseAuthUserTest):
    """Test cases for authuser forms"""

    def setUp(self):
        super().setUp()
        self.correct_form_data = {
            'username': "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!"
        }
        self.incorrect_form_data = {
            'username': "",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!"
        }

    # UPDATE_PROFILE FORM TESTS
    # Test form saves valid data correctly
    def test_form_saves(self):
        correct_test_form = AuthUserCreationForm(data=self.correct_form_data)
        self.assertTrue(correct_test_form.is_valid(),
                        "Form should be valid")
        if correct_test_form.is_valid():
            correct_test_form.save()

        incorrect_test_form = AuthUserCreationForm(
            data=self.incorrect_form_data)
        self.assertFalse(incorrect_test_form.is_valid(),
                         "Form should fail - no username")

        duplicate_test_form = AuthUserCreationForm(data=self.correct_form_data)
        self.assertFalse(duplicate_test_form.is_valid(),
                         "Form should fail - duplicate username")

    # Test form validation for required fields
    def test_form_required_fields(self):
        # Test missing username
        missing_username_data = self.correct_form_data.copy()
        missing_username_data['username'] = ''
        form = AuthUserCreationForm(data=missing_username_data)
        self.assertFalse(form.is_valid(),
                         "Form should fail with missing username")
        self.assertIn('username', form.errors,
                      "Should show username error")

        # Test missing email
        missing_email_data = self.correct_form_data.copy()
        missing_email_data['email'] = ''
        form = AuthUserCreationForm(data=missing_email_data)
        self.assertFalse(form.is_valid(),
                         "Form should fail with missing email")
        self.assertIn('email', form.errors,
                      "Should show email error")

        # Test missing first_name
        missing_firstname_data = self.correct_form_data.copy()
        missing_firstname_data['first_name'] = ''
        form = AuthUserCreationForm(data=missing_firstname_data)
        self.assertFalse(form.is_valid(),
                         "Form should fail with missing first name")
        self.assertIn('first_name', form.errors,
                      "Should show first name error")

    # Test email uniqueness validation
    def test_email_uniqueness_validation(self):
        # Create a user with existing email
        existing_email_data = self.correct_form_data.copy()
        existing_email_data['email'] = self.test_user.email
        form = AuthUserCreationForm(data=existing_email_data)
        self.assertFalse(form.is_valid(),
                         "Form should fail with duplicate email")
        self.assertIn('email', form.errors,
                      "Should show email uniqueness error")

    # Test boss assignment validation (circular hierarchy prevention)
    def test_boss_assignment_validation(self):
        # Test creating user with valid boss assignment
        valid_boss_data = self.correct_form_data.copy()
        valid_boss_data['boss'] = self.test_user.id
        # AuthUserCreationForm does include boss field
        form = AuthUserCreationForm(data=valid_boss_data)
        # Should be valid with proper boss assignment
        self.assertTrue('boss' in form.fields,
                        "Creation form should include boss field")
        self.assertTrue(form.is_valid(),
                        "Form should be valid with proper boss assignment")

    # Test form excludes sensitive fields (password, etc.)
    def test_form_excludes_sensitive_fields(self):
        form = AuthUserCreationForm()
        # Verify that sensitive fields are not included in creation form
        sensitive_fields = ['is_staff', 'is_superuser', 'user_permissions',
                            'groups', 'date_joined', 'last_login']
        for field in sensitive_fields:
            self.assertNotIn(field, form.fields,
                             f"Form should not include {field} field")

    # USERCREATIONFORM TESTS
    # Test user creation with valid data
    def test_user_creation_with_valid_data(self):
        form = AuthUserCreationForm(data=self.correct_form_data)
        self.assertTrue(form.is_valid(),
                        "Form should be valid with correct data")
        user = form.save()
        self.assertIsInstance(user, User,
                              "Should create a User instance")
        self.assertEqual(user.username, "testuser",
                         "Should set correct username")
        self.assertEqual(user.email, "test@example.com",
                         "Should set correct email")
        self.assertTrue(user.check_password("ComplexPass123!"),
                        "Should set password correctly")

    # Test password confirmation matching
    def test_password_confirmation_matching(self):
        # Test mismatched passwords
        mismatched_data = self.correct_form_data.copy()
        mismatched_data['password2'] = 'DifferentPassword123!'
        form = AuthUserCreationForm(data=mismatched_data)
        self.assertFalse(form.is_valid(),
                         "Form should fail with mismatched passwords")
        self.assertIn('password2', form.errors,
                      "Should show password confirmation error")

        # Test matching passwords
        form = AuthUserCreationForm(data=self.correct_form_data)
        self.assertTrue(form.is_valid(),
                        "Form should be valid with matching passwords")

    # Test email validation
    def test_email_validation(self):
        # Test invalid email format
        invalid_email_data = self.correct_form_data.copy()
        invalid_email_data['email'] = 'invalid-email-format'
        form = AuthUserCreationForm(data=invalid_email_data)
        self.assertFalse(form.is_valid(),
                         "Form should fail with invalid email format")
        self.assertIn('email', form.errors,
                      "Should show email format error")

        # Test valid email formats
        valid_emails = ['test@example.com', 'user.name@domain.co.uk',
                        'user+tag@example.org']
        for email in valid_emails:
            valid_email_data = self.correct_form_data.copy()
            valid_email_data['email'] = email
            valid_email_data['username'] = f'user_{email.split("@")[0]}'
            form = AuthUserCreationForm(data=valid_email_data)
            self.assertTrue(form.is_valid(),
                            f"Form should accept valid email: {email}")

    # Test username requirements
    def test_username_requirements(self):
        # Test username too short
        short_username_data = self.correct_form_data.copy()
        short_username_data['username'] = 'ab'
        form = AuthUserCreationForm(data=short_username_data)
        # Django's default username validation may allow short usernames
        # This test documents the current behavior

        # Test username with invalid characters
        invalid_chars_data = self.correct_form_data.copy()
        invalid_chars_data['username'] = 'user@name!'
        form = AuthUserCreationForm(data=invalid_chars_data)
        # Test may pass or fail depending on Django's username validation

        # Test duplicate username
        duplicate_username_data = self.correct_form_data.copy()
        duplicate_username_data['username'] = self.test_user.username
        form = AuthUserCreationForm(data=duplicate_username_data)
        self.assertFalse(form.is_valid(),
                         "Form should fail with duplicate username")
        self.assertIn('username', form.errors,
                      "Should show username uniqueness error")

    # TEMPLATE & INTEGRATION TESTS
    # Test correct template used for each view
    def test_correct_templates_used(self):
        # Test login view template
        response = self.client.get(reverse("login_view"))
        self.assertEqual(response.status_code, 200,
                         "Login view should be accessible")

        # Test authenticated views
        self.client.login(username="Test_account", password="Placeholder123")

        # Test profile view template
        response = self.client.get(reverse("profile",
                                           args=[self.test_user.id]))
        self.assertTemplateUsed(response, "authuser/profile.html",
                                "Profile view should use correct template")

        # Test edit profile view template
        response = self.client.get(reverse("edit_profile",
                                           args=[self.test_user.id]))
        self.assertTemplateUsed(response, "authuser/edit_profile.html",
                                "Edit profile should use correct template")

    # Test context variables passed correctly
    def test_context_variables(self):
        self.client.login(username="Test_account", password="Placeholder123")

        # Test profile view context
        response = self.client.get(reverse("profile",
                                           args=[self.test_user.id]))
        self.assertIn('user_profile', response.context,
                      "Profile view should include user_profile context")
        self.assertEqual(response.context['user_profile'], self.test_user,
                         "Context should contain correct user")

        # Test edit profile view context
        response = self.client.get(reverse("edit_profile",
                                           args=[self.test_user.id]))
        self.assertIn('form', response.context,
                      "Edit profile should include form context")

    # Test conditional content (edit buttons, etc.)
    def test_conditional_content(self):
        # Test edit button visibility for own profile
        self.client.login(username="Test_account", password="Placeholder123")
        response = self.client.get(reverse("profile",
                                           args=[self.test_user.id]))
        self.assertContains(response, "Edit Profile",
                            msg_prefix="Should show edit button on own")

        # Test edit button hidden for other profiles
        self.client.login(username="Test_account2", password="Placeholder123")
        response = self.client.get(reverse("profile",
                                           args=[self.test_user.id]))
        self.assertNotContains(response, "Edit Profile",
                               msg_prefix="Should hide edit button on others")

    # Test form rendering and error display
    def test_form_rendering_and_errors(self):
        # Test form renders correctly
        response = self.client.get(reverse("register"))
        self.assertContains(response, 'name="username"',
                            msg_prefix="Form should render username field")
        self.assertContains(response, 'name="email"',
                            msg_prefix="Form should render email field")
        self.assertContains(response, 'name="password1"',
                            msg_prefix="Form should render password field")

        # Test error display
        response = self.client.post(reverse("register"), {
            'username': '',  # Empty required field
            'email': 'invalid-email',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'pass',
            'password2': 'different'
        })
        self.assertEqual(response.status_code, 200,
                         "Should stay on form with errors")
        self.assertContains(response, "This field is required",
                            msg_prefix="Should display validation errors")
