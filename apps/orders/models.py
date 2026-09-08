from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q
from django.conf import settings
from decimal import Decimal

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
        models.CheckConstraint(
            condition=Q(quantity__gte=1),
            name="cart_item_quantity_gte_1"
        ),
        models.UniqueConstraint(
            fields=["product", "cart"],
            name="unique_cart_product"
        )
    ]


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        EXPIRED = "expired", "Expired"
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(total_price__gte=Decimal("0.01")),
                name="order_total_price_gte_001"
            )
        ]


class OrderItem(models.Model):
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey("catalog.Product", on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(unit_price__gte=Decimal("0.01")),
                name="order_item_unit_price_gte_001"
            ),
            models.CheckConstraint(
                condition=Q(quantity__gte=1),
                name="order_item_quantity_gte_1"
            ),
            models.UniqueConstraint(
                fields=["product", "order"],
                name="unique_product_order"
            )
        ]