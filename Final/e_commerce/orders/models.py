from authentication.models import User
from django.core.validators import MinValueValidator
from django.db import models
from products.models import Product

# Create your models here.


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CREATED = "created", "Created"
        PAID = "paid", "Paid"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELED = "canceled", "Canceled"

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders", db_index=True
    )
    order_status = models.CharField(
        max_length=20, choices=OrderStatus, default=OrderStatus.CREATED, db_index=True
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id}"

    def calculate_total_amount(self):
        return sum(item.quantity * item.price for item in self.items.all())


class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", db_index=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OrderItem {self.id}"


class ShoppingCart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shopping_cart", db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE, related_name="items", db_index=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CartItem {self.id}"

    def is_available(self):
        return self.product.stock_quantity >= self.quantity


class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = (
            "credit_card",
            "Credit card",
        )
        DEBIT_CARD = (
            "debit_card",
            "Debit card",
        )
        DIGITAL_WALLET = (
            "digital_wallet",
            "Digital Wallet",
        )
        BANK = "bank", "Bank"

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        related_name="payments",
        null=True,
        db_index=True,
    )
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethod, db_index=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus,
        default=PaymentStatus.PENDING,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id}"
