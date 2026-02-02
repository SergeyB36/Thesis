from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase

from employees.models import Employee
from tasks import services
from tasks.models import Task
from tasks.serializers import TasksSerializer


class TaskModelTest(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(name="Иван Иванов", is_active=True)
        self.task = Task.objects.create(
            title="Тестовая задача",
            description="Описание",
            assignee=self.employee,
            deadline=timezone.now().date() + timezone.timedelta(days=7),
            status=Task.Status.TODO,
            priority=Task.Priority.MEDIUM,
        )

    def test_task_str_representation(self):
        self.assertIn("Тестовая задача", str(self.task))
        self.assertIn(str(self.task.deadline), str(self.task))
        self.assertIn(str(self.task.assignee), str(self.task))

    def test_get_possible_assignees(self):
        assignees = services.get_possible_assignees()
        self.assertIn(self.employee, assignees)

    def test_complete_task_changes_status(self):
        services.complete_task(self.task.id)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.DONE)
        self.assertIsNotNone(self.task.completed_at)

    def test_get_critical_tasks(self):
        critical_task = Task.objects.create(
            title="Критическая задача",
            description="Описание",
            assignee=self.employee,
            deadline=timezone.now().date() + timezone.timedelta(days=5),
            status=Task.Status.TODO,
            priority=Task.Priority.CRITICAL,
        )
        critical_tasks = services.get_critical_tasks()
        self.assertIn(critical_task, critical_tasks)


class TasksSerializerTest(APITestCase):

    def setUp(self):
        self.employee = Employee.objects.create(name="Петр Петров", is_active=True)
        self.task = Task.objects.create(
            title="Задача",
            description="Описание",
            assignee=self.employee,
            deadline=timezone.now().date() + timezone.timedelta(days=3),
            status=Task.Status.TODO,
            priority=Task.Priority.HIGH,
        )

    def test_serializer_fields(self):
        serializer = TasksSerializer(instance=self.task)
        data = serializer.data
        self.assertEqual(
            set(data.keys()), {"title", "description", "parent_task", "assignee", "deadline", "status", "priority"}
        )
        self.assertEqual(data["title"], self.task.title)
        self.assertEqual(data["assignee"], self.task.assignee.id)


class FunctionsTest(TestCase):
    def setUp(self):
        self.employee1 = Employee.objects.create(name="Работник 1", is_active=True)
        self.employee2 = Employee.objects.create(name="Работник 2", is_active=True)
        # Создаем задачи для нагрузки
        Task.objects.create(
            title="Задача 1",
            assignee=self.employee1,
            deadline=timezone.now().date(),
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.MEDIUM,
        )
        Task.objects.create(
            title="Задача 2",
            assignee=self.employee1,
            deadline=timezone.now().date(),
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.MEDIUM,
        )
        Task.objects.create(
            title="Задача 3",
            assignee=self.employee2,
            deadline=timezone.now().date(),
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.MEDIUM,
        )

    def test_get_possible_assignees(self):
        assignees = services.get_possible_assignees()
        # Минимальная нагрузка у employee2 (1 задача)
        self.assertIn(self.employee2, assignees)
        # employee1 имеет 2 задачи, и возможно он тоже есть, т.к. ограничение +2
        self.assertIn(self.employee1, assignees)

    def test_complete_task_function(self):
        task = Task.objects.create(
            title="Задача для завершения",
            assignee=self.employee1,
            deadline=timezone.now().date() + timezone.timedelta(days=1),
            status=Task.Status.IN_PROGRESS,
        )
        services.complete_task(task.id)
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.DONE)
        self.assertIsNotNone(task.completed_at)
