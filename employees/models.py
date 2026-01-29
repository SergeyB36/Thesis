from django.db import models

from config import settings


class Employee(models.Model):
    fullname = models.CharField(max_length=300, verbose_name="Ф.И.О.", help_text="Иванов Иван Иванович")
    uniquename = models.CharField(unique=True, max_length=50, verbose_name="Уникальный идентификатор сотрудника")
    position = models.CharField(max_length=300, verbose_name="Должность", help_text="Сотрудник")
    avatar = models.ImageField(upload_to="employees/image", blank=True, null=True, verbose_name="Фото")
    work_phone = models.IntegerField(blank=True, null=True, verbose_name="Служебный телефон")
    description = models.TextField(blank=False, verbose_name="Примечание")
    header = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Руководитель сотрудника", on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создание учетной карточки")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")
    is_active = models.BooleanField(default=True, verbose_name="Статус активности")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"Курс '{self.fullname}'"
