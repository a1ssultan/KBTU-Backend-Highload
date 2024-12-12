from django.urls import path
from wishlists.views import ClearWishlistView, WishlistView

urlpatterns = [
    path("", WishlistView.as_view(), name="wishlist"),
    path("clear/", ClearWishlistView.as_view(), name="wishlist-clear"),
]
