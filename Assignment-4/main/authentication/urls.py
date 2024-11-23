from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register'),
]
