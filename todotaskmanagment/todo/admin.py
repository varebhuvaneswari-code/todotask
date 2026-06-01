from django.contrib import admin

from .models import ActivityLog, Category, Priority, TodoTask


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "color")
    ordering = ("level",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "color", "created_at")
    search_fields = ("name", "user__username")


@admin.register(TodoTask)
class TodoTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "completed", "priority", "category", "due_date")
    list_filter = ("status", "completed", "priority", "category")
    search_fields = ("title", "description", "user__username")
    date_hierarchy = "created_at"


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("user", "task", "action", "created_at")
    search_fields = ("action", "user__username", "task__title")
