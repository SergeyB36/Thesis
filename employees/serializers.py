from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from employees.models import Employee
from tasks.models import Task
from tasks.serializers import TasksSerializer


class EmployeeSerializer(ModelSerializer):
    task_count = SerializerMethodField()
    tasks = TasksSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = (
            "fullname",
            "uniquename",
            "position",
            "avatar",
            "work_phone",
            "phone",
            "description",
            "header",
            "created_at",
            "updated_at",
            "is_active",
            "task_count",
            "tasks",
        )

    read_only_fields = [
        "created_at",
        "updated_at",
        "is_active",
        "header",
        "tasks",
    ]

    def get_task_count(self, obj):
        """Количество задач сотрудника"""
        return obj.tasks.filter(status=Task.Status.IN_PROGRESS).count()


class EmployeeForTask(Serializer):
    task_id = serializers.IntegerField()
