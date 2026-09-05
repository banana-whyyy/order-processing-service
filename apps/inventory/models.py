from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator

from ..catalog.models import Product



class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gte=0),
                name="inventory_quantity_gte_0"
            )
        ]