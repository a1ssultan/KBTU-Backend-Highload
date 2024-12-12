from rest_framework import serializers
from .models import Order, OrderItem, Payment, ShoppingCart, CartItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_status', 'total_amount', 'items', 'created_at', 'updated_at']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'created_at', 'updated_at']
        extra_kwargs = {
            'cart': {'read_only': True},
        }


class ShoppingCartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'read_only': True},
        }


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'payment_method', 'amount', 'status', 'created_at', 'updated_at']

    def validate(self, data):
        if data['amount'] > data['order'].total_amount:
            raise serializers.ValidationError("Payment amount exceeds order total")
        return data
