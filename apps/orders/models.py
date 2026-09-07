from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q
from django.conf import settings

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