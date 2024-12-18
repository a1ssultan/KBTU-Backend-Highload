from authentication.models import User
from django.db import models
from products.models import Product

# Create your models here.


class Wishlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="wishlists", db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wishlist {self.id}"


class WishlistItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, related_name="items", db_index=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WishlistItem {self.id}"
