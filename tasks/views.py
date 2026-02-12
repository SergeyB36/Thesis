from django.db.models import Case, IntegerField, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from employees.models import Employee
from employees.permissions import IsOwner
from tasks.models import Task
from tasks.paginators import MyPaginator
from tasks.serializers import (
    CriticalTasksSerializer,
    GetTasksSerializer,
    TasksSerializer,
)
from tasks.services import get_tesk_to_work


class TaskCreateAPIView(CreateAPIView):
    """Для всех публичных привычек"""

    queryset = Task.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskListAPIView(ListAPIView):
    """Список задач в работе отсортированный по приоритету"""

    queryset = Task.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MyPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "title", "parent_task", "deadline", "priority"]

    def get_queryset(self):
        """Функция сортировки задач по приоритету"""
        qs = super().get_queryset()

        qs = (
            qs.filter(status=Task.Status.IN_PROGRESS, owner=self.request.user)
            .annotate(
                priority_rank=Case(
                    When(priority=Task.Priority.CRITICAL, then=0),
                    When(priority=Task.Priority.HIGH, then=1),
                    When(priority=Task.Priority.MEDIUM, then=2),
                    When(priority=Task.Priority.LOW, then=3),
                    default=4,
                    output_field=IntegerField(),
                )
            )
            .order_by("priority_rank")
        )
        return qs


class TaskRetrieveAPIView(RetrieveAPIView):
    """Просмотр задачи"""

    queryset = Task.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsOwner]


class TaskDestroyAPIView(DestroyAPIView):
    """Удаление задачи. Возможно только с выполненными задачами"""

    queryset = Task.objects.filter(status=Task.Status.DONE)
    serializer_class = TasksSerializer
    permission_classes = [IsOwner]


class TaskUpdateAPIView(UpdateAPIView):
    """Обновление задачи"""

    queryset = Task.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsOwner]


class GetTaskAPIView(GenericAPIView):
    """Назначает сотрудника для выполнения задачи"""

    serializer_class = GetTasksSerializer
    permission_classes = [IsOwner]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task_id = serializer.validated_data["task_id"]
        employer_id = serializer.validated_data["employer_id"]
        try:
            get_tesk_to_work(employer_id, task_id)
        except Task.DoesNotExist:
            raise exceptions.ValidationError("Task not found")
        except Employee.DoesNotExist:
            raise exceptions.ValidationError("Employee not found")
        return Response(status=204)


class CriticalTaskListAPIView(ListAPIView):
    """Список важных задач"""

    queryset = Task.objects.filter(priority=Task.Priority.CRITICAL)
    serializer_class = CriticalTasksSerializer
    permission_classes = [IsOwner]


class WarningTaskListAPIView(ListAPIView):

    serializer_class = TasksSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = Task.objects.filter(status=Task.Status.TODO, subtasks__status=Task.Status.IN_PROGRESS).distinct()
        return qs
