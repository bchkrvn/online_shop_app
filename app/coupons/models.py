from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(100)],
                                   help_text='Значение в процентах от 0 до 100')
    active = models.BooleanField()

    def save(self, *args, **kwargs):
        if self.valid_from and self.valid_to:
            if self.valid_from > self.valid_to:
                raise ValidationError("Date to can't be late then date from")
        super(Coupon, self).save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['code'])
        ]
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return f'Coupon {self.code}'
