from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee
from tasks.models import Task

User = get_user_model()


class TaskModelTest(APITestCase):

    def setUp(self):
        # Создаем сотрудника
        self.employee = Employee.objects.create(
            fullname="Иван Иванович Иванов", is_active=True, uniquename="Иваныч", position="Менеджер"
        )

        # Создаем начальника (1)
        self.url = reverse("users:register")
        self.user = User.objects.create(fullname="testuser", email="testuser@test.com")
        self.user.set_password("1234")
        self.user.save()
        # Создаем начальника (2)
        self.url = reverse("users:register")
        self.user = User.objects.create(fullname="testuser1", email="testuser1@test.com")
        self.user.set_password("1234")
        self.user.save()

    def test_task_create(self):
        """Тест: создание задачи"""
        # Создание задачи
        self.url1 = reverse("tasks:task-create")
        user = User.objects.get(fullname="testuser1")
        self.client.force_authenticate(user=user)
        deadline = timezone.now().date() + timezone.timedelta(days=7)
        response = self.client.post(
            self.url1,
            {
                "title": "Тестовая родительская задача",
                "description": "Описание",
                "owner": user.id,
                "deadline": deadline,
                "status": Task.Status.TODO,
                "priority": Task.Priority.MEDIUM,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Тестовая родительская задача")
        self.assertEqual(response.data["owner"], user.id)
        task = Task.objects.get(title="Тестовая родительская задача")

        # Добавление исполнителя задаче
        self.assertEqual(task.assignee, None)
        emp = Employee.objects.get(uniquename="Иваныч")
        self.url2 = reverse("tasks:get-task")
        response = self.client.post(self.url2, {"employer_id": emp.id, "task_id": task.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        task = Task.objects.get(title="Тестовая родительская задача")
        self.assertEqual(task.assignee, emp)

    def test_task_create_invalid_data(self):
        """Тест: некорректные данные при создании задачи"""
        self.url1 = reverse("tasks:task-create")
        user = User.objects.get(fullname="testuser1")
        self.client.force_authenticate(user=user)
        response = self.client.post(
            self.url1,
            {},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_task_create_not_auth(self):
        """Тест: создание задачи без аутентификации"""
        self.url1 = reverse("tasks:task-create")
        user = User.objects.get(fullname="testuser1")
        deadline = timezone.now().date() + timezone.timedelta(days=7)
        response = self.client.post(
            self.url1,
            {
                "title": "Тестовая родительская задача",
                "description": "Описание",
                "owner": user.id,
                "deadline": deadline,
                "status": Task.Status.TODO,
                "priority": Task.Priority.MEDIUM,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
