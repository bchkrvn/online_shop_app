from django import forms
from orders.models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['city', 'address', 'postal_code']
        # labels = {
        #     "address": "Адрес",
        #     "postal_code": "Почтовый индекс",
        #     "city": "Город",
        # }
