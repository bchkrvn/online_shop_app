from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Coupon(models.Model):
    code = models.CharField(_('Промокод'), max_length=50, unique=True)
    valid_from = models.DateTimeField(_('Действителен от'))
    valid_to = models.DateTimeField(_('Действителен до'))
    discount = models.IntegerField(_('Скидка'), validators=[MinValueValidator(0),
                                                            MaxValueValidator(100)],
                                   help_text=_('Значение в процентах от 0 до 100'))
    active = models.BooleanField(_('Активен'))

    def save(self, *args, **kwargs):
        if self.valid_from and self.valid_to:
            if self.valid_from > self.valid_to:
                raise ValidationError(_("Дата начала действия не может быть позже окончания"))
        super(Coupon, self).save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['code'])
        ]
        verbose_name = _('Купон')
        verbose_name_plural = _('Купоны')

    def __str__(self):
        return f'Coupon {self.code}'
