from django.contrib import admin

from authentication.models import User


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "phone_number", "is_staff", "is_active")
    search_fields = ("username",)
