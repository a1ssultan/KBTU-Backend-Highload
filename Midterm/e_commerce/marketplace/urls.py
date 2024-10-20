from django.urls import path
from .views import (
    ProductList,
    CategoryList,
    OrderList,
    OrderDetail,
    OrderItemAdd,
    OrderItemDelete,
    OrderItemClear,
)

urlpatterns = [
    path("products/", ProductList.as_view(), name="product-list"),
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("orders/", OrderList.as_view(), name="order-list"),
    path("orders/<int:order_id>/", OrderDetail.as_view(), name="order-detail"),
    path("orders/<int:order_id>/items/", OrderItemAdd.as_view(), name="order-item-add"),
    path(
        "orders/<int:order_id>/items/<int:item_id>/",
        OrderItemDelete.as_view(),
        name="order-item-delete",
    ),
    path(
        "orders/<int:order_id>/clear/",
        OrderItemClear.as_view(),
        name="order-item-clear",
    ),
]
