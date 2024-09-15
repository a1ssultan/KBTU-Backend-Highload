from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.all_posts, name='posts'),
    path('posts/edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('posts/delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('posts/details/<int:pk>', views.details, name='post_details'),
    path('posts/<int:pk>/add-comment/', views.add_comment, name='add_comment'),
    path('posts/add-post/', views.form, name='add_post'),
]
