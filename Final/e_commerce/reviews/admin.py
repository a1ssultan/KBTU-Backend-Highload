from django.contrib import admin
from reviews.models import Review

# Register your models here.


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "user",
        "rating",
        "comment",
        "created_at",
        "updated_at",
    )
    search_fields = ("product__name", "user__email", "comment")
    list_filter = ("rating", "created_at")
    ordering = ("-created_at",)
