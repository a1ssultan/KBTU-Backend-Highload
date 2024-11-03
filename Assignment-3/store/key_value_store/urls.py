from django.urls import path
from .views import KeyValueViewSet

urlpatterns = [
    path('key-value/', KeyValueViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('key-value/<str:key>/', KeyValueViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'})),
]
