from django.db import transaction
from orders.models import CartItem, Order, Payment, ShoppingCart
from orders.serializers import (
    CartItemSerializer,
    OrderSerializer,
    PaymentSerializer,
    ShoppingCartSerializer,
)
from products.models import Product
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product").select_related("user")
    serializer_class = OrderSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.order_status in [
            Order.OrderStatus.CANCELED,
            Order.OrderStatus.DELIVERED,
        ]:
            return Response(
                {"error": "Cannot cancel this order"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order.order_status = Order.OrderStatus.CANCELED
        order.save()
        return Response({"status": "Order canceled"}, status=status.HTTP_200_OK)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.prefetch_related("items__product").select_related(
        "user"
    )
    serializer_class = ShoppingCartSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @transaction.atomic
    @action(detail=True, methods=["post"])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        product_id = request.data.get("product")
        quantity = request.data.get("quantity", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock_quantity:
                return Response(
                    {"error": f"Not enough stock for product {product.name}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("order")
    serializer_class = PaymentSerializer
