from django.urls import path
from wishlists.views import WishlistView, ClearWishlistView

urlpatterns = [
    path("", WishlistView.as_view(), name="wishlist"),
    path("clear/", ClearWishlistView.as_view(), name="wishlist-clear"),
]
