from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

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
            "owner",
        )

        validators = [
            DeadlineValidator(field="deadline"),
        ]


class GetTasksSerializer(Serializer):
    task_id = serializers.IntegerField()
    employer_id = serializers.IntegerField()


class CriticalTasksSerializer(ModelSerializer):
    fullname = serializers.CharField(source="assignee__fullname")

    class Meta:
        model = Task

        fields = (
            "title",
            "deadline",
            "fullname",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["string_output"] = f"{instance.itle}, {instance.deadline}, {instance.assignee.fullname}"
        return data
