from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'user', 'address', 'postal_code',
                    'city', 'created', 'updated', 'paid']
    list_filter = ['paid', 'created', 'updated', 'user']
    list_editable = ['paid']
    inlines = [OrderItemInline]
