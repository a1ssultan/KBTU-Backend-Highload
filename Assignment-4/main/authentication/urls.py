from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register'),

    # Token Authentication URLs
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # UserProfile API URLs
    path('profiles/', UserProfileListView.as_view(), name='user-profile-list'),
    path('profiles/<int:pk>/', UserProfileDetailView.as_view(), name='user-profile-detail'),
]
