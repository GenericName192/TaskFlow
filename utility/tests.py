from django.test import TestCase
from authuser.models import User
from task.models import Task
from task.forms import TaskForm
from .utils import (
    Can_assign_task, can_be_boss, get_all_team_tasks,
    mass_create_tasks, calculate_user_task_statistics
)
from datetime import date, timedelta


class BaseUtilityTest(TestCase):
    """Base class with common setUp for utility tests"""
    def setUp(self):
        """Set up test data for utility function testing"""
        # Create hierarchical user structure
        self.ceo = User.objects.create(
            username="ceo_user",
            first_name="CEO",
            last_name="Boss",
            email="ceo@test.com",
            boss=None
        )

        self.manager = User.objects.create(
            username="manager_user",
            first_name="Manager",
            last_name="Lead",
            email="manager@test.com",
            boss=self.ceo
        )

        self.employee = User.objects.create(
            username="employee_user",
            first_name="Employee",
            last_name="Worker",
            email="employee@test.com",
            boss=self.manager
        )

        self.other_employee = User.objects.create(
            username="other_employee",
            first_name="Other",
            last_name="Worker",
            email="other@test.com",
            boss=self.manager
        )

        self.external_user = User.objects.create(
            username="external_user",
            first_name="External",
            last_name="Person",
            email="external@test.com",
            boss=None
        )

        # Create test tasks
        self.task1 = Task.objects.create(
            title="Employee Task 1",
            description="First task for employee",
            assigned_to=self.employee,
            created_by=self.manager,
            completed=False
        )

        self.task2 = Task.objects.create(
            title="Employee Task 2",
            description="Second task for employee",
            assigned_to=self.employee,
            created_by=self.manager,
            completed=True
        )

        self.task3 = Task.objects.create(
            title="Other Employee Task",
            description="Task for other employee",
            assigned_to=self.other_employee,
            created_by=self.manager,
            completed=False
        )


class CanAssignTaskTest(BaseUtilityTest):
    """Test cases for Can_assign_task function"""

    # Test manager can assign to subordinate
    def test_manager_can_assign_to_subordinate(self):
        result = Can_assign_task(self.employee, self.manager)
        self.assertTrue(result)

    # Test CEO can assign to anyone in hierarchy
    def test_ceo_can_assign_to_hierarchy(self):
        result = Can_assign_task(self.manager, self.ceo)
        self.assertTrue(result)
        result = Can_assign_task(self.employee, self.ceo)
        self.assertTrue(result)

    # Test user can assign to themselves
    def test_user_can_assign_to_self(self):
        result = Can_assign_task(self.employee, self.employee)
        self.assertTrue(result)

    # Test cannot assign to non-subordinate
    def test_cannot_assign_to_non_subordinate(self):
        result = Can_assign_task(self.external_user, self.manager)
        self.assertFalse(result)

    # Test subordinate cannot assign to manager
    def test_subordinate_cannot_assign_to_manager(self):
        result = Can_assign_task(self.manager, self.employee)
        self.assertFalse(result)


class CanBeBossTest(BaseUtilityTest):
    """Test cases for can_be_boss function"""

    # Test valid boss assignment
    def test_valid_boss_assignment(self):
        # Employee can have CEO as boss (no circular hierarchy)
        result = can_be_boss(self.employee, self.ceo)
        self.assertTrue(result)

    # Test None boss is always valid
    def test_none_boss_valid(self):
        result = can_be_boss(self.employee, None)
        self.assertTrue(result)

    # Test circular hierarchy prevention
    def test_prevents_circular_hierarchy(self):
        # Manager cannot have employee as boss (would create circle)
        result = can_be_boss(self.manager, self.employee)
        self.assertFalse(result)

    # Test self-assignment prevention
    def test_prevents_self_boss(self):
        # User cannot be their own boss
        result = can_be_boss(self.employee, self.employee)
        self.assertFalse(result)


class GetAllTeamTasksTest(BaseUtilityTest):
    """Test cases for get_all_team_tasks function"""

    # Test manager gets all team tasks
    def test_manager_gets_team_tasks(self):
        result = get_all_team_tasks(self.manager)

        # Should include manager's own tasks and subordinates' tasks
        self.assertIn(self.manager.full_name, result)
        self.assertIn(self.employee.full_name, result)
        self.assertIn(self.other_employee.full_name, result)

        # Check task counts
        employee_tasks = list(result[self.employee.full_name])
        self.assertEqual(len(employee_tasks), 2)  # task1 and task2

    # Test employee gets only own tasks
    def test_employee_gets_own_tasks(self):
        result = get_all_team_tasks(self.employee)

        # Should only include employee's own tasks
        self.assertIn(self.employee.full_name, result)
        self.assertEqual(len(result), 1)  # Only employee, no subordinates

        employee_tasks = list(result[self.employee.full_name])
        self.assertEqual(len(employee_tasks), 2)


class MassCreateTasksTest(BaseUtilityTest):
    """Test cases for mass_create_tasks function"""

    # Test successful mass task creation
    def test_successful_mass_creation(self):
        user_list = [self.employee, self.other_employee]
        form_data = {
            'title': 'Mass Created Task',
            'description': 'Task created for multiple users',
            'due_date': (date.today() + timedelta(days=1)).isoformat()
        }
        form = TaskForm(data=form_data)

        success, message = mass_create_tasks(user_list, form, self.manager)

        self.assertTrue(success)
        self.assertIn(self.employee.full_name, message)
        self.assertIn(self.other_employee.full_name, message)

        # Verify tasks were created
        new_tasks = Task.objects.filter(title='Mass Created Task')
        self.assertEqual(new_tasks.count(), 2)

    # Test empty user list
    def test_empty_user_list(self):
        form_data = {'title': 'Test Task', 'description': 'Test'}
        form = TaskForm(data=form_data)

        success, message = mass_create_tasks([], form, self.manager)

        self.assertFalse(success)
        self.assertIn("empty list", message)

    # Test invalid form
    def test_invalid_form(self):
        user_list = [self.employee]
        form_data = {'title': '', 'description': 'Test'}  # Missing title
        form = TaskForm(data=form_data)

        success, message = mass_create_tasks(user_list, form, self.manager)

        self.assertFalse(success)
        self.assertIn("invalid", message)

    # Test permission failure
    def test_permission_failure(self):
        # Manager cannot assign to external user
        user_list = [self.external_user]
        form_data = {'title': 'Test Task', 'description': 'Test'}
        form = TaskForm(data=form_data)

        success, message = mass_create_tasks(user_list, form, self.manager)

        self.assertFalse(success)
        self.assertIn("failed", message)


class CalculateUserTaskStatisticsTest(BaseUtilityTest):
    """Test cases for calculate_user_task_statistics function"""

    # Test basic statistics calculation
    def test_basic_statistics(self):
        result = calculate_user_task_statistics(self.employee)

        self.assertEqual(result['total_tasks_count'], 2)
        self.assertEqual(result['completed_tasks_count'], 1)
        self.assertEqual(result['total_ongoing_tasks'], 1)

        # Check upcoming tasks
        upcoming = list(result['up_coming_tasks'])
        self.assertEqual(len(upcoming), 1)
        self.assertEqual(upcoming[0].title, "Employee Task 1")

    # Test user with no tasks
    def test_user_with_no_tasks(self):
        result = calculate_user_task_statistics(self.external_user)

        self.assertEqual(result['total_tasks_count'], 0)
        self.assertEqual(result['completed_tasks_count'], 0)
        self.assertEqual(result['total_ongoing_tasks'], 0)
        self.assertEqual(len(list(result['up_coming_tasks'])), 0)

    # Test user with only completed tasks
    def test_user_with_only_completed_tasks(self):
        # Mark employee's remaining task as completed
        self.task1.completed = True
        self.task1.save()

        result = calculate_user_task_statistics(self.employee)

        self.assertEqual(result['total_tasks_count'], 2)
        self.assertEqual(result['completed_tasks_count'], 2)
        self.assertEqual(result['total_ongoing_tasks'], 0)
        self.assertEqual(len(list(result['up_coming_tasks'])), 0)
