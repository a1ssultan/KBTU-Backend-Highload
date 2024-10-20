from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from marketplace.models import Product, Category, Order, OrderItem
from marketplace.serializers import ProductSerializer, CategorySerializer, OrderSerializer, OrderItemSerializer


class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderList(APIView):
    def get(self, request):
        orders = request.user.orders.prefetch_related('items__product').all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Order, pk=pk, user=self.request.user)

    def get(self, request, order_id):
        order = self.get_object(order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def delete(self, request, order_id):
        order = self.get_object(order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemAdd(APIView):
    def post(self, request, order_id):
        order = get_object_or_404(Order.objects.prefetch_related('items'), pk=order_id, user=request.user)
        product = get_object_or_404(Product, pk=request.data['product_id'])
        quantity = request.data.get('quantity', 1)

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
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemClear(APIView):
    def delete(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id, user=request.user)
        order.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
