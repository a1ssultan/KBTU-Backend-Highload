from django.contrib import admin

from orders.models import Order, OrderItem, ShoppingCart, CartItem, Payment


# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "order_status",
        "total_amount",
        "created_at",
        "updated_at",
    )
    search_fields = ("user__email",)
    list_filter = ("order_status", "created_at")
    ordering = ("-created_at",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
        "created_at",
        "updated_at",
    )
    search_fields = ("order__id", "product__name")
    ordering = ("-created_at",)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "updated_at")
    search_fields = ("user__email",)
    ordering = ("-created_at",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity", "created_at", "updated_at")
    search_fields = ("cart__id", "product__name")
    ordering = ("-created_at",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "payment_method",
        "amount",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("order__id",)
    list_filter = ("payment_method", "status")
    ordering = ("-created_at",)
