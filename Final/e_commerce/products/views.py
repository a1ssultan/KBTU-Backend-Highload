from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from reviews.models import Review
from reviews.serializers import ReviewSerializer


class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.prefetch_related("products")
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.prefetch_related("products")
    serializer_class = CategorySerializer


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer


class ProductReviewsView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.select_related("product", "user").filter(
            product__id=self.kwargs["pk"]
        )
