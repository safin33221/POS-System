
from django.db import transaction

from apps.products.models import Product
from .models import StockMovement


@transaction.atomic
def add_stock(product, quantity, note=""):
    """
    Add stock to a product.
    """

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    product.stock += quantity
    product.save(update_fields=["stock", "updated_at"])

    StockMovement.objects.create(
        product=product,
        movement_type="IN",
        quantity=quantity,
        note=note,
    )

    return product


@transaction.atomic
def remove_stock(product, quantity, note=""):
    """
    Remove stock from a product.
    """

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    if product.stock < quantity:
        raise ValueError("Insufficient stock.")

    product.stock -= quantity
    product.save(update_fields=["stock", "updated_at"])

    StockMovement.objects.create(
        product=product,
        movement_type="OUT",
        quantity=quantity,
        note=note,
    )

    return product
