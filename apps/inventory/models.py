from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator


class Inventory(models.Model):
    product = models.OneToOneField("catalog.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gte=0),
                name="inventory_quantity_gte_0"
            )
        ]


class StockReservation(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        EXPIRED = "expired", "Expired"

    order_item = models.OneToOneField("orders.OrderItem", on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gte=1),
                name="reservation_quantity_gte_1"
            )
        ]