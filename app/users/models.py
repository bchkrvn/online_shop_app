from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class Roles(models.TextChoices):
    BUYER = 'buyer', "Покупатель"
    MODERATOR = 'moderator', "Модератор"
    ADMIN = 'admin', "ADMIN"


class User(AbstractUser):
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.BUYER)
    birth_date = models.DateField(_('Дата рождения'), null=True, blank=True)
    username = models.CharField(
        _('Имя пользователя'),
        max_length=150,
        unique=True,
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("Имя пользователя занято"),
        }, )

    REQUIRED_FIELDS = ["email", 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'User({self.username})'
