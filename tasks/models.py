from django.conf import settings
from django.db import models

from employees.models import Employee


class Task(models.Model):
    """Модель задачи"""

    class Status(models.TextChoices):
        TODO = "todo", "К выполнению"
        IN_PROGRESS = "in_progress", "В работе"
        REVIEW = "review", "На проверке"
        DONE = "done", "Выполнено"
        CANCELLED = "cancelled", "Отменено"

    class Priority(models.TextChoices):
        LOW = "low", "Низкий"
        MEDIUM = "medium", "Средний"
        HIGH = "high", "Высокий"
        CRITICAL = "critical", "Критический"

    title = models.CharField(verbose_name="Наименование задачи", max_length=200, help_text="Краткое описание задачи")

    description = models.TextField(
        verbose_name="Описание задачи", blank=True, null=True, help_text="Подробное описание задачи"
    )

    parent_task = models.ForeignKey(
        "self",
        verbose_name="Родительская задача",
        on_delete=models.CASCADE,
        related_name="subtasks",
        blank=True,
        null=True,
        help_text="Задача, от которой зависит текущая",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="task", verbose_name="Владелец задачи"
    )
    assignee = models.ForeignKey(
        Employee,
        verbose_name="Исполнитель",
        on_delete=models.SET_NULL,
        related_name="tasks",
        blank=True,
        null=True,
        help_text="Сотрудник, ответственный за выполнение задачи",
    )

    deadline = models.DateField(
        verbose_name="Срок выполнения", help_text="Дата, к которой задача должна быть выполнена"
    )

    status = models.CharField(verbose_name="Статус", max_length=20, choices=Status.choices, default=Status.TODO)

    priority = models.CharField(
        verbose_name="Приоритет", max_length=20, choices=Priority.choices, default=Priority.MEDIUM
    )

    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    completed_at = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title}, {self.deadline}, {self.assignee}"
