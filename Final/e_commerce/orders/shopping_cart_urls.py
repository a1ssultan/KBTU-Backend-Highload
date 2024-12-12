from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShoppingCartViewSet

router = DefaultRouter()
router.register(r'', ShoppingCartViewSet, basename='shopping_cart')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/add-item/', ShoppingCartViewSet.as_view({'post': 'add_item'}), name='add-item'),
]
