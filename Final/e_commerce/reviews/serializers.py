from rest_framework import serializers
from authentication.models import User
from products.models import Product
from reviews.models import Review


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]


class UserReviewSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name", "email"]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class ReviewSerializer(serializers.ModelSerializer):
    product = ProductReviewSerializer(read_only=True)
    user = UserReviewSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class CreateUpdateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["product", "rating", "comment"]

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
