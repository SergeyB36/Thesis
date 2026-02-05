from django.db.models import Count

from employees.models import Employee
from tasks.models import Task


def get_possible_assignees(task_id, user_id):
    """Получение возможных исполнителей для задачи"""
    user = Employee.objects.get(id=user_id)
    employees = (
        Employee.objects.filter(is_active=True, header=user)
        .annotate(active_tasks_count=Count("tasks"))
        .order_by("active_tasks_count")
    )
    if not employees.exists():
        return []
    min_loaded = employees.first().active_tasks_count
    possible_assignees = []
    possible_assignees.append(employees.first())
    try:
        task = Task.objects.get(id=task_id)
        parent_task_assignee = task.parent_task.assignee if task.parent_task else None
    except Task.DoesNotExist:
        parent_task_assignee = None
    if parent_task_assignee:
        parent_employee = employees.filter(id=parent_task_assignee.id).first()
        if parent_employee and parent_employee.active_tasks_count <= min_loaded + 2:
            possible_assignees.append(parent_task_assignee)
    return set(possible_assignees)
