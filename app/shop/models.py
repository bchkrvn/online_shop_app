from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(_('Название'), max_length=200)
    slug = models.SlugField(_('Слаг'), max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(_('Категория'), Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(_('Название'), max_length=200)
    slug = models.SlugField(_('Слаг'), max_length=200)
    image = models.ImageField(_('Изображение'), upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(_('Описание'), blank=True)
    price = models.DecimalField(_('Цена'), max_digits=10, decimal_places=2)
    available = models.BooleanField(_('Наличие'), default=True)
    created = models.DateTimeField(_('Создано'), auto_now_add=True)
    updated = models.DateTimeField(_('Обновлено'), auto_now=True)
    quantity = models.PositiveIntegerField(_('Количество'), default=0)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.available = False
        else:
            self.available = True
        super().save(*args, **kwargs)

