from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator

from decimal import Decimal


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2, 
        validators=[MinValueValidator(Decimal("0.01"))],

    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(price__gte=Decimal("0.01")),
                name="product_price_gte_001"
            )
        ]