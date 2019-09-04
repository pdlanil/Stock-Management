from django.db import models
from product.models import Product


class Stock(models.Model):
    quantity = models.PositiveIntegerField()
    sales = models.PositiveIntegerField(null=True,blank=True)
    remaining = models.PositiveIntegerField(null=True,blank=True)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return 'Id:{0} Products:{1}'.format(self.id, self.product_id)


