from rest_framework.viewsets import ModelViewSet

from employees.models import Employee
from employees.serializers import EmployeeSerializer


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        serializer.save(header=self.request.user)

    def get_queryset(self):
        queryset = Employee.objects.all()
        user = self.request.user
        queryset = queryset.filter(is_active=True, header=user)
        return queryset
