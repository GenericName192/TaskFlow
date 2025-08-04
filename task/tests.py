from django.test import TestCase, Client
from django.urls import reverse
from authuser.models import User
from .models import Task
from .forms import TaskForm
from datetime import date, timedelta


class BaseTaskTest(TestCase):
    """Base class with common setUp for task tests"""
    def setUp(self):
        """Set up test data"""
        # Create test users
        self.boss = User.objects.create(
            username="boss_user",
            first_name="Boss",
            last_name="Manager",
            email="boss@test.com",
            boss=None
        )
        self.boss.set_password("TestPass123")
        self.boss.save()

        self.employee = User.objects.create(
            username="employee_user",
            first_name="Employee",
            last_name="Worker",
            email="employee@test.com",
            boss=self.boss
        )
        self.employee.set_password("TestPass123")
        self.employee.save()

        self.other_user = User.objects.create(
            username="other_user",
            first_name="Other",
            last_name="Person",
            email="other@test.com",
            boss=None
        )
        self.other_user.set_password("TestPass123")
        self.other_user.save()

        # Create test tasks
        self.task1 = Task.objects.create(
            title="Test Task 1",
            description="First test task",
            assigned_to=self.employee,
            created_by=self.boss,
            completed=False
        )

        self.task2 = Task.objects.create(
            title="Test Task 2",
            description="Second test task",
            assigned_to=self.employee,
            created_by=self.boss,
            completed=True
        )

        self.client = Client()


class TaskModelTest(BaseTaskTest):
    """Test cases for the Task model"""

    # Test task creation
    def test_task_creation(self):
        task = Task.objects.create(
            title="New Task",
            description="Task description",
            assigned_to=self.employee,
            created_by=self.boss
        )
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, "New Task")
        self.assertEqual(task.assigned_to, self.employee)
        self.assertEqual(task.created_by, self.boss)
        self.assertFalse(task.completed)  # Default value

    # Test task string representation
    def test_task_str(self):
        self.assertEqual(str(self.task1), "Test Task 1")

    # Test task completion toggle
    def test_task_completion(self):
        self.assertFalse(self.task1.completed)
        self.task1.completed = True
        self.task1.save()
        self.assertTrue(self.task1.completed)


class TaskViewTest(BaseTaskTest):
    """Test cases for task views"""

    # Test task list view access
    def test_task_list_authenticated(self):
        self.client.login(username="boss_user", password="TestPass123")
        response = self.client.get(reverse("task_list",
                                           args=[self.employee.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task 1")
        self.assertContains(response, "Test Task 2")

    # Test task list requires login
    def test_task_list_requires_login(self):
        response = self.client.get(reverse("task_list",
                                   args=[self.employee.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    # Test task creation via POST
    def test_task_creation_via_post(self):
        self.client.login(username="boss_user", password="TestPass123")
        task_data = {
            'title': 'New Task via POST',
            'description': 'Created through form',
            'due_date': ''
        }
        response = self.client.post(reverse("task_list",
                                    args=[self.employee.id]),
                                    task_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects
                        .filter(title='New Task via POST').exists())

    # Test toggle task completion
    def test_toggle_task_completion(self):
        self.client.login(username="employee_user", password="TestPass123")
        # Task starts as incomplete
        self.assertFalse(self.task1.completed)

        response = self.client.get(reverse("toggle_complete",
                                   args=[self.task1.id]))
        self.assertEqual(response.status_code, 302)

        # Refresh from database
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.completed)

    # Test task details view
    def test_task_details_view(self):
        self.client.login(username="boss_user", password="TestPass123")
        response = self.client.get(reverse("task_details",
                                   args=[self.task1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.title)
        self.assertContains(response, self.task1.description)

    # Test task update permission
    def test_task_update_permission(self):
        # Creator should be able to update
        self.client.login(username="boss_user", password="TestPass123")
        response = self.client.get(reverse("update_task",
                                   args=[self.task1.id]))
        self.assertEqual(response.status_code, 200)

        # Assigned user should be able to update
        self.client.login(username="employee_user", password="TestPass123")
        response = self.client.get(reverse("update_task",
                                   args=[self.task1.id]))
        self.assertEqual(response.status_code, 200)

    # Test task delete permission
    def test_task_delete_permission(self):
        # Only creator should be able to delete
        self.client.login(username="boss_user", password="TestPass123")
        response = self.client.get(reverse("delete_task",
                                           args=[self.task1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())


class TaskFormTest(BaseTaskTest):
    """Test cases for task forms"""

    # Test valid form data
    def test_valid_form(self):
        form_data = {
            'title': 'Form Test Task',
            'description': 'Testing form validation',
            'due_date': (date.today() + timedelta(days=1)).isoformat()
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Test form validation - past due date
    def test_form_past_due_date_validation(self):
        form_data = {
            'title': 'Past Due Task',
            'description': 'This should fail validation',
            'due_date': (date.today() - timedelta(days=1)).isoformat()
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)

    # Test form validation - required fields
    def test_form_required_fields(self):
        form_data = {
            'title': '',  # Required field left empty
            'description': 'Description here',
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    # Test form saves correctly
    def test_form_save(self):
        form_data = {
            'title': 'Saved Task',
            'description': 'This task should save',
            'due_date': ''
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Save with additional required fields
        task = form.save(commit=False)
        task.assigned_to = self.employee
        task.created_by = self.boss
        task.save()

        self.assertEqual(task.title, 'Saved Task')
        self.assertEqual(task.assigned_to, self.employee)
        self.assertEqual(task.created_by, self.boss)
