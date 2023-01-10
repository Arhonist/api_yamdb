from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    bio = models.TextField(
        blank=True, verbose_name='О себе'
    )
    role = models.CharField(
        choices=UserRole.choices,
        default=UserRole.USER,
        max_length=40,
        verbose_name='Роль пользователя'
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        max_length=254,
        verbose_name='Электронная почта'
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']
