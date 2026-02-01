from django.db import models

from employees.models import Employee
from tasks.models import Task


def get_possible_assignees(self):
    """
    Получение возможных исполнителей для задачи
    Используется для эндпоинта важных задач
    """
    from django.db.models import Count

    # Получаем всех активных сотрудников с количеством их активных задач
    employees = Employee.objects.filter(is_active=True).annotate(active_tasks_count=Count("tasks"))

    if not employees.exists():
        return []

    # Наименее загруженный сотрудник
    min_loaded = employees.first().active_tasks_count

    # Если есть родительская задача и исполнитель
    possible_assignees = []

    # Добавляем наименее загруженных сотрудников
    for employee in employees:
        if employee.active_tasks_count <= min_loaded + 2:
            possible_assignees.append(employee)

    return possible_assignees

def comlete_task(task_id):
    """Функция изменения задачи после выполнения"""
    task = Task.objects.get(id=task_id)
    task.status = Task.Status.DONE
    task.save()
