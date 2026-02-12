from employees.models import Employee
from tasks.models import Task


def get_tesk_to_work(user_id, task_id):
    task = Task.objects.get(id=task_id)
    task.assignee = Employee.objects.get(id=user_id)
    task.status = Task.Status.IN_PROGRESS
    task.save()
