from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
def isPositive(value):
    if value<0:
        raise ValidationError(f"value must be greater than 0 or in positive number")

class Product(models.Model):
    name = models.CharField(max_length=30)
    brand = models.CharField(max_length=30, null=True, blank=True)
    total_price = models.FloatField(validators=[isPositive])

    def __str__(self):
        return self.name


