from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from reviews.models import Review
from reviews.serializers import ReviewSerializer, CreateUpdateReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CreateUpdateReviewSerializer
        return ReviewSerializer

    def get_queryset(self):
        if self.request.method == 'GET' and not self.kwargs.get('pk'):
            return Review.objects.filter(user=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

