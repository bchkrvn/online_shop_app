from _decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from coupons.models import Coupon
from shop.models import Product
from users.models import User


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, null=True,
                             blank=True)
    address = models.CharField(_('Адрес'), max_length=250)
    postal_code = models.CharField(_('Почтовый индекс'), max_length=20)
    city = models.CharField(_('Город'), max_length=100)
    created = models.DateTimeField(_('Создан'), auto_now_add=True)
    updated = models.DateTimeField(_('Обновлен'), auto_now=True)
    paid = models.BooleanField(_('Оплачен'), default=False)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(_('Скидка'), default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')

    def __str__(self):
        return f'Order {self.pk}'

    def get_total_cost(self) -> Decimal:
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_total_cost_before_discount(self) -> Decimal:
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self) -> Decimal:
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return Decimal(round(total_cost * (self.discount / Decimal(100)), 2))
        return Decimal(0)

    def get_absolute_url(self):
        return reverse('orders:order_detail', args=[self.pk])

    def get_created_date(self):
        return self.created.strftime("%d.%m.%Y")


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(_('Цена'), max_digits=10, decimal_places=2)

    quantity = models.PositiveIntegerField(_('Количество'), default=1)

    def __str__(self):
        return str(self.pk)

    def get_cost(self) -> Decimal:
        return self.price * self.quantity

    class Meta:
        verbose_name = _('Позиция заказа')
        verbose_name_plural = _('Позиции заказа')
