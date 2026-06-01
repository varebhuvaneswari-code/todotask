from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "dark_mode", "updated_at")
    search_fields = ("user__username", "user__email", "full_name")
