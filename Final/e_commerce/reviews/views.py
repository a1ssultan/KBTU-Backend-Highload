from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from reviews.models import Review
from reviews.serializers import CreateUpdateReviewSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.select_related("product", "user")

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return CreateUpdateReviewSerializer
        return ReviewSerializer

    def get_queryset(self):
        if self.request.method == "GET" and not self.kwargs.get("pk"):
            return (
                Review.objects.filter(user=self.request.user)
                .select_related("product")
                .order_by("-created_at")
            )
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
