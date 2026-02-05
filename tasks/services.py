from employees.models import Employee
from tasks.models import Task


def get_tesk_to_work(user_id, task_id):
    task = Task.objects.get(id=task_id)
    task.assignee = Employee.objects.get(id=user_id)
    task.status = Task.Status.IN_PROGRESS
    task.save()


def get_tasks():
    """Запрашивает из БД задачи, которые не взяты в работу, но от которых зависят другие задачи, взятые в работу"""
    warning_tasks = Task.objects.filter(status=Task.Status.TODO, parent_task__isnull=False).exclude(
        parent_task__status=Task.Status.TODO
    )
    return warning_tasks
