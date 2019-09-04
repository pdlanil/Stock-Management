from django.db import models
from django.utils import timezone
from customer.models import Customer
from product.models import Product
from django.core.exceptions import ValidationError

def isPositive(value):
    if value<0:
        raise ValidationError(f"value must be greater than 0 or in positive number")

class Purchase(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pieces = models.PositiveIntegerField()
    price = models.FloatField(validators=[isPositive])
    rate = models.FloatField(validators=[isPositive])
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return '{0}'.format(self.customer_id)

