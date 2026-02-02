from django.db.models import Case, IntegerField, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from tasks.models import Task
from tasks.serializers import TasksSerializer


class TaskCreateAPIView(CreateAPIView):
    """Для всех публичных привычек"""

    queryset = Task.objects.all()
    serializer_class = TasksSerializer


class TaskListAPIView(ListAPIView):
    """Список задач в работе отсортированный по приоритету"""

    serializer_class = TasksSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "title", "parent_task", "deadline", "priority"]

    def get_queryset(self):
        """Функция сортировки по приоритету"""
        return (
            Task.objects.filter(status=Task.Status.IN_PROGRESS)
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


class TaskRetrieveAPIView(RetrieveAPIView):
    """Просмотр задачи"""

    queryset = Task.objects.all()
    serializer_class = TasksSerializer


class TaskDestroyAPIView(DestroyAPIView):
    """Удаление задачи. Возможно только с выполненными задачами"""

    queryset = Task.objects.filter(status=Task.Status.DONE)
    serializer_class = TasksSerializer


class TaskUpdateAPIView(UpdateAPIView):
    """Обновление задачи"""

    queryset = Task.objects.all()
    serializer_class = TasksSerializer
