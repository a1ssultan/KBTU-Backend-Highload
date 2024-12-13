from django.contrib.auth import get_user_model
from orders.models import CartItem, Order, Payment, ShoppingCart
from products.models import Category, Product
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password123"
        )
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=100.00,
            stock_quantity=10,
            category=self.category,
        )
        self.order = Order.objects.create(user=self.user, total_amount=100)

    def test_create_order(self):
        data = {"total_amount": 100}
        response = self.client.post("/api/orders/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cancel_order(self):
        response = self.client.post(f"/api/orders/{self.order.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_status, Order.OrderStatus.CANCELED)

    def test_invalid_cancel_order(self):
        self.order.order_status = Order.OrderStatus.DELIVERED
        self.order.save()
        response = self.client.post(f"/api/orders/{self.order.id}/cancel/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ShoppingCartViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password123"
        )
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=100.00,
            stock_quantity=10,
            category=self.category,
        )
        self.cart = ShoppingCart.objects.create(user=self.user)

    def test_add_item_to_cart(self):
        data = {"product": self.product.id, "quantity": 2}
        response = self.client.post(
            f"/api/shopping-cart/{self.cart.id}/add-item/", data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart_item = CartItem.objects.get(cart=self.cart, product=self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_add_item_with_insufficient_stock(self):
        data = {"product": self.product.id, "quantity": 15}
        response = self.client.post(
            f"/api/shopping-cart/{self.cart.id}/add-item/", data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PaymentViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password123"
        )
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=100.00,
            stock_quantity=10,
            category=self.category,
        )
        self.order = Order.objects.create(user=self.user, total_amount=100)

    def test_create_payment(self):
        data = {
            "order": self.order.id,
            "payment_method": "Credit Card",
            "amount": 100.00,
            "status": "PAID",
        }
        response = self.client.post("/api/payments/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payment = Payment.objects.get(order=self.order)
        self.assertEqual(payment.amount, 100.00)

    def test_create_payment_exceeding_order_total(self):
        data = {
            "order": self.order.id,
            "payment_method": "Credit Card",
            "amount": 200.00,
            "status": "PAID",
        }
        response = self.client.post("/api/payments/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
