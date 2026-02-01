from rest_framework.serializers import ModelSerializer

from tasks.models import Task
from tasks.validators import DeadlineValidator


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

        validators = [
            DeadlineValidator(field="deadline"),
        ]
