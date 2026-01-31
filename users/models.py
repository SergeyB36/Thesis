"""Модель пользователя"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    fullname = models.CharField(max_length=50, verbose_name="Ф.И.О.", help_text="Иванов Иван Иванович")
    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    avatar = models.ImageField(upload_to="users/image", blank=True, null=True, verbose_name="Аватар")
    token = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.fullname
