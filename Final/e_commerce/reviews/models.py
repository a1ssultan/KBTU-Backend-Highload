from authentication.models import User
from django.db import models
from products.models import Product

# Create your models here.


class Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews", db_index=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews", db_index=True
    )
    rating = models.IntegerField(db_index=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review {self.id}"
