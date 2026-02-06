from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from employees.models import Employee
from employees.serializers import EmployeeForTask, EmployeeSerializer
from employees.servises import get_possible_assignees
from tasks.permissions import IsOwner


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        serializer.save(header=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        qs = qs.filter(is_active=True, header=user)
        return qs

    def list(self, request, **kwargs):
        assignee = request.query_params.get("assignee", "false").lower() == "true"
        if assignee:
            serializer = EmployeeForTask(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            task_id = serializer.validated_data["task_id"]
            possible_employees = get_possible_assignees(task_id, user_id=request.user.id)
            return Response(EmployeeSerializer(possible_employees, many=True).data)
        else:
            queryset = Employee.objects.filter(is_active=True, header=self.request.user)
            serializer = EmployeeSerializer(queryset, many=True)
            return Response(serializer.data)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == "list":
            permission_classes = [IsAuthenticated]
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        if self.action == "retrieve":
            permission_classes = [IsOwner]
        if self.action == "update":
            permission_classes = [IsOwner]
        if self.action == "partial_update":
            permission_classes = [IsOwner]
        if self.action == "destroy":
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]
