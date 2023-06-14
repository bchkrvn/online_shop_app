from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Заказ №{order_id}'
    message = f'{order.user.first_name} {order.user.last_name} \n' \
              f'Вы успешно оформили заказ в магазине Семерочка. \n' \
              f'Номер вашего заказа - {order_id}.\n' \
              f'Адрес доставки: {order.postal_code}, г. {order.city}, {order.address}\n\n' \
              f'Ваш заказ:\n'

    for i, item in enumerate(order.items.all(), 1):
        message += f'{i}) {item.product} - {item.quantity} шт.\n'

    message += f"\nОбщая стоимость - {order.get_total_cost()} ₽"

    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.user.email])
    return mail_sent
