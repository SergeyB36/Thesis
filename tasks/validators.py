import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone


class DeadlineValidator:
    """Валидатор дедлайна задачи"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        validated_value = value.get(self.field)
        if validated_value:
            now = timezone.now().date()
            if isinstance(validated_value, datetime.datetime):
                deadline_date = validated_value.date()
            elif isinstance(validated_value, datetime.date):
                deadline_date = validated_value
            else:
                raise ValidationError("Неверный формат даты дедлайна")

            if deadline_date > now:
                return
            else:
                raise ValidationError("На выполнение задачи должен быть выделен хотя бы 1 день")
        else:
            raise ValidationError("Дедлайн не указан")
