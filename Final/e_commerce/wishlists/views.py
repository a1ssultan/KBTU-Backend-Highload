from django.db import transaction
from products.models import Product
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from wishlists.models import Wishlist, WishlistItem
from wishlists.serializers import WishlistItemSerializer, WishlistSerializer


class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist, created = Wishlist.objects.prefetch_related("items__product").get_or_create(user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        product_id = request.data.get("product")
        if not product_id:
            return Response(
                {"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        wishlist, created = Wishlist.objects.prefetch_related("items").get_or_create(user=request.user)
        wishlist_item, created = WishlistItem.objects.get_or_create(
            wishlist=wishlist, product=product
        )

        if not created:
            return Response(
                {"error": "Product is already in the wishlist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            WishlistItemSerializer(wishlist_item).data, status=status.HTTP_201_CREATED
        )

    @transaction.atomic
    def delete(self, request):
        product_id = request.data.get("product")
        if not product_id:
            return Response(
                {"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        wishlist, created = Wishlist.objects.prefetch_related("items").get_or_create(user=request.user)
        try:
            wishlist_item = WishlistItem.objects.get(
                wishlist=wishlist, product_id=product_id
            )
            wishlist_item.delete()
            return Response(
                {"message": "Product removed from wishlist"}, status=status.HTTP_200_OK
            )
        except WishlistItem.DoesNotExist:
            return Response(
                {"error": "Product not found in the wishlist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ClearWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        wishlist, created = Wishlist.objects.prefetch_related("items").get_or_create(user=request.user)
        wishlist.items.all().delete()
        return Response({"message": "Wishlist cleared"}, status=status.HTTP_200_OK)

