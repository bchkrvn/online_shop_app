from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.TextChoices):
    BUYER = 'buyer', "Покупатель"
    MODERATOR = 'moderator', "Модератор"
    ADMIN = 'admin', "ADMIN"


class User(AbstractUser):
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.BUYER)
    birth_date = models.DateField(null=True, blank=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },)

    REQUIRED_FIELDS = ["email", 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        # self.set_password(self.password)
        super().save()

    def __str__(self):
        return f'User({self.username})'
