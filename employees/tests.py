from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee
from tasks.models import Task

User = get_user_model()


class EmployeeModelTest(APITestCase):
    def setUp(self):
        # Создаем пользователя - руководителя
        self.user = User.objects.create(fullname="testuser", email="testuser@test.com")
        # Создаем сотрудника
        self.employee = Employee.objects.create(
            fullname="Иван Иванович",
            uniquename="Иваныч",
            position="Разработчик",
            description="Описание сотрудника",
            header=self.user,
        )

    def test_employee_creation(self):
        self.assertEqual(self.employee.fullname, "Иван Иванович")
        self.assertEqual(self.employee.position, "Разработчик")
        self.assertEqual(self.employee.header, self.user)
        self.assertTrue(self.employee.is_active)


class EmployeeViewSetTest(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create(fullname="testuser", email="testuser@test.com")
        self.other_user = User.objects.create(fullname="testuser1", email="testuser1@test.com")

        # Создаем сотрудника
        self.employee = Employee.objects.create(
            fullname="Иван Иванович",
            uniquename="Иваныч",
            position="Разработчик",
            description="Описание",
            header=self.user,
        )
        self.employee1 = Employee.objects.create(
            fullname="Иван Петрович",
            uniquename="Петрович",
            position="Разработчик",
            description="Описание сотрудника",
            header=self.user,
        )

        self.employee2 = Employee.objects.create(
            fullname="Иван Романович",
            uniquename="Романыч",
            position="Разработчик",
            description="Описание сотрудника",
            header=self.user,
        )

        self.task = Task.objects.create(
            title="Задача 1",
            assignee=self.employee,
            deadline=timezone.now().date() + timezone.timedelta(days=7),
            owner=self.user,
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.CRITICAL,
        )
        self.task1 = Task.objects.create(
            title="Задача 2",
            assignee=self.employee1,
            deadline=timezone.now().date() + timezone.timedelta(days=7),
            owner=self.user,
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.MEDIUM,
        )

        self.task3 = Task.objects.create(
            title="Задача 3",
            deadline=timezone.now().date() + timezone.timedelta(days=7),
            owner=self.user,
            parent_task=self.task1,
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.LOW,
        )

        self.task4 = Task.objects.create(
            title="Задача 4",
            deadline=timezone.now().date() + timezone.timedelta(days=7),
            owner=self.user,
            assignee=self.employee,
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.LOW,
        )
        self.task5 = Task.objects.create(
            title="Задача 5",
            deadline=timezone.now().date() + timezone.timedelta(days=7),
            owner=self.user,
            assignee=self.employee,
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.LOW,
        )
        self.task6 = Task.objects.create(
            title="Задача 6",
            deadline=timezone.now().date() + timezone.timedelta(days=7),
            owner=self.user,
            assignee=self.employee,
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.LOW,
        )

        self.url = reverse("employees:employee-list")

    def test_list_employees(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        # Проверка содержания данных
        self.assertTrue(any(emp["uniquename"] == "Иваныч" for emp in response.data))

    def test_create_employee(self):
        self.client.force_authenticate(user=self.user)
        # url = reverse("employees:employee-create")
        data = {
            "fullname": "Петр Петрович",
            "uniquename": "Петрович2",
            "position": "Менеджер",
            "description": "Описание менеджера",
        }
        self.assertEqual(Employee.objects.count(), 3)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 4)
        self.assertEqual(Employee.objects.get(uniquename="Петрович2").fullname, "Петр Петрович")

    def test_list_permission_for_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_with_assignee_param(self):
        self.client.force_authenticate(user=self.user)
        params = {
            "assignee": "true",
            "task_id": self.task3.id,
        }
        response = self.client.get(self.url, query_params=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
