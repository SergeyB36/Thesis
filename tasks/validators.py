from django.utils import timezone
from rest_framework.exceptions import ValidationError


class DeadlineValidator:
    """Валидатор дедлайна задачи"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        validated_value = value.get(self.field)
        if validated_value:
            now = timezone.now().date()
            deadline_date = validated_value.date()
            if deadline_date > now:
                return
            else:
                raise ValidationError("На выполнение задачи должен быть выделен хотя бы 1 день")
        else:
            raise ValidationError("Дедлайн не указан")
