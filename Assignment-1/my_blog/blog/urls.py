from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('posts/', views.all_posts, name='posts'),
    path('posts/edit/<int:pk>/', views.edit_post, name='edit-post'),
    path('posts/delete/<int:pk>/', views.delete_post, name='delete-post'),
    path('posts/details/<int:pk>', views.details, name='details'),
    path('posts/<int:pk>/add-comment/', views.add_comment, name='add_comment'),
    path('add-post/', views.form, name='add-post'),
]
