from django.urls import path

from products.views import CategoryListView, CategoryDetailView, ProductListView, ProductDetailView, ProductReviewsView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/reviews/', ProductReviewsView.as_view(), name='product-reviews'),
]
