from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from employees.models import Employee
from tasks.models import Task


class TasksSerializer(ModelSerializer):

    class Meta:
        model = Task

        fields = (
            "title",
            "description",
            "parent_task",
            "assignee",
            "deadline",
            "status",
            "priority",
        )

        read_only_fields = [
            "assignee",
            "deadline",
            "priority",
        ]
