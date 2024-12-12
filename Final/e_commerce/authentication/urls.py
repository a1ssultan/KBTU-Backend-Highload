from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path

from authentication.views import CustomTokenObtainPairView, UserViewSet, RegisterViewSet

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "register/", RegisterViewSet.as_view({"post": "create"}), name="user-register"
    ),
    path(
        "users/",
        UserViewSet.as_view({"get": "list", "put": "update", "delete": "destroy"}),
        name="user-actions",
    ),
]
