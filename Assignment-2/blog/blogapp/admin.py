from django.contrib import admin

from .models import User, Post, Tag, Comment


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "bio"]
    search_fields = ["username", "email"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_at"]
    search_fields = ["title"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display =["author", "post", "created_at"]
