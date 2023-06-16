import redis
from django.conf import settings
from .models import Product

rs = redis.Redis(host=settings.REDIS_HOST,
                 port=settings.REDIS_PORT,
                 db=settings.REDIS_DB)


class Recommender:
    def get_product_key(self, id_: int):
        return f'product:{id_}:purchased_with'

    def products_bought(self, products: list[Product]):
        products_ids = [product.pk for product in products]

        for product1_id in products_ids:

            for product2_id in products_ids:

                if product2_id != product1_id:
                    rs.zincrby(self.get_product_key(product1_id), 1, product2_id)

    def submit_products_for(self, products, max_results=3):
        products_ids = [product.pk for product in products]

        # Если только один товар:
        if len(products_ids) == 1:
            product_id = products_ids[0]
            suggestions = rs.zrange(self.get_product_key(product_id),
                                    0, -1, desc=True)[:max_results]

        # Если несколько:
        else:
            flat_ids = ''.join([str(p_id) for p_id in products_ids])
            tmp_key = f'tmp_{flat_ids}'

            keys = [self.get_product_key(p_id) for p_id in products_ids]
            rs.zunionstore(tmp_key, keys)
            rs.zrem(tmp_key, *products_ids)
            suggestions = rs.zrange(tmp_key, 0, -1, desc=True)
            rs.delete(tmp_key)

        suggestions_product_ids = [int(p_id) for p_id in suggestions]
        suggestions_product_list = list(Product.objects.filter(id__in=suggestions_product_ids))
        suggestions_product_list.sort(key=lambda x: suggestions_product_ids.index(x.id))

        return suggestions_product_list

    def clean_purchases(self):
        for p_id in Product.objects.value_list('id', flat=True):
            rs.delete(self.get_product_key(p_id))
