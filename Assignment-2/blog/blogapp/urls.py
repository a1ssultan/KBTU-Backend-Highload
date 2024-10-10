from django.urls import path
from . import views
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path("posts/", views.PostsView.as_view(), name='posts'),
    path("posts/<int:pk>", views.post_detail, name="post_detail"),
    path("posts-2/", views.all_posts, name='posts-2')
] + debug_toolbar_urls()
