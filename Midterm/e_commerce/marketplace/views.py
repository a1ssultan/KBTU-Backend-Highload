from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from marketplace.models import Product, Category, Order, OrderItem
from marketplace.serializers import ProductSerializer, CategorySerializer, OrderSerializer, OrderItemSerializer


class ProductList(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request):
        products = cache.get("cached_products")
        if products:
            return Response(products, status=status.HTTP_200_OK)
        products = Product.objects.select_related("category").all()
        serializer = ProductSerializer(products, many=True)
        cache.set("cached_products", serializer.data, timeout=60 * 15)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryList(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request):
        categories = cache.get("cached_categories")
        if categories:
            return Response(categories, status=status.HTTP_200_OK)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        cache.set("cached_categories", serializer.data, timeout=60 * 15)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderList(APIView):
    def get(self, request):
        cache_key = f"cached_orders_user_id_{request.user.id}"
        orders = cache.get(cache_key)
        if orders:
            return Response(orders, status=status.HTTP_200_OK)

        orders = request.user.orders.prefetch_related('items__product').all()
        serializer = OrderSerializer(orders, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 15)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            cache.delete(f"cached_orders_user_id_{request.user.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Order.objects.select_related("user"), pk=pk, user=self.request.user)

    def get(self, request, order_id):
        cache_key = f"cached_order_{order_id}_user_{request.user.id}"
        order = cache.get(cache_key)
        if order:
            return Response(order, status=status.HTTP_200_OK)

        order = self.get_object(order_id)
        serializer = OrderSerializer(order)
        cache.set(cache_key, serializer.data, timeout=60 * 15)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, order_id):
        order = self.get_object(order_id)
        order.delete()
        cache.delete(f"cached_order_{order_id}_user_{request.user.id}")
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemAdd(APIView):
    def post(self, request, order_id):
        order = get_object_or_404(Order.objects.prefetch_related('items'), pk=order_id, user=request.user)
        product = get_object_or_404(Product, pk=request.data['product_id'])
        quantity = request.data.get('quantity', 1)

        cache_key = f"cached_order_{order_id}_user_{request.user.id}"
        cache.delete(cache_key)

        serializer = OrderItemSerializer(data={'order': order.id, 'product': product.id, 'quantity': quantity})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrderItemDelete(APIView):
    def delete(self, request, order_id, item_id):
        order = get_object_or_404(Order, pk=order_id, user=request.user)
        order_item = get_object_or_404(OrderItem, pk=item_id, order=order)
        order_item.delete()

        cache_key = f"cached_order_{order_id}_user_{request.user.id}"
        cache.delete(cache_key)

        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemClear(APIView):
    def delete(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id, user=request.user)
        order.items.all().delete()

        cache_key = f'cached_order_{order_id}_user_{request.user.id}'
        cache.delete(cache_key)

        return Response(status=status.HTTP_204_NO_CONTENT)
