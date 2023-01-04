from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    bio = models.TextField(
        blank=True, verbose_name='bio'
    )
    role = models.CharField(
        choices=UserRole.choices,
        default=UserRole.USER,
        max_length=40,
        verbose_name='role'
    )
    email = models.EmailField(
        unique=True, blank=False, verbose_name='email'
    )

    def __str__(self):
        return self.username
