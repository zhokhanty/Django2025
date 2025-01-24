from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Task, Project, Category, Priority

User = get_user_model()


class RoleBasedAccessControlTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='admin123', role='admin')
        self.manager_user = User.objects.create_user(username='manager', password='manager123', role='manager')
        self.employee_user = User.objects.create_user(username='employee', password='employee123', role='employee')

        self.project = Project.objects.create(
            name="Test Project",
            description="A test project.",
            start_date="2025-01-01",
            end_date="2025-12-31"
        )
        self.category = Category.objects.create(name="Bug Fix")
        self.priority = Priority.objects.create(level="High")
        self.task = Task.objects.create(
            title="Test Task",
            description="A test task for employees.",
            project=self.project,
            category=self.category,
            priority=self.priority,
            assignee=self.employee_user,
            due_date="2025-02-01"
        )

    def test_admin_access(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.post('/api/users/', {
            'username': 'new_user',
            'password': 'password123',
            'role': 'employee'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/api/projects/', {
            'name': 'New Project',
            'description': 'A new test project.',
            'start_date': '2025-01-01',
            'end_date': '2025-12-31'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_manager_access(self):
        self.client.login(username='manager', password='manager123')
        response = self.client.post('/api/projects/', {
            'name': 'Another Project',
            'description': 'Another test project.',
            'start_date': '2025-01-01',
            'end_date': '2025-12-31'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/api/users/', {
            'username': 'unauthorized_user',
            'password': 'password123',
            'role': 'employee'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_access(self):
        self.client.login(username='employee', password='employee123')
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post('/api/projects/', {
            'name': 'Unauthorized Project',
            'description': 'An unauthorized test project.',
            'start_date': '2025-01-01',
            'end_date': '2025-12-31'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post('/api/users/', {
            'username': 'unauthorized_user',
            'password': 'password123',
            'role': 'employee'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)