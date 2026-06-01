from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Priority(models.Model):
    name = models.CharField(max_length=20, unique=True)
    level = models.PositiveSmallIntegerField(unique=True)
    color = models.CharField(max_length=20, default="secondary")

    class Meta:
        ordering = ("level",)
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.name


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=80)
    color = models.CharField(max_length=20, default="#2563eb")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name")
        ordering = ("name",)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class TodoTask(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="todos")
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(blank=True, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("completed", "due_date", "-created_at")
        indexes = [
            models.Index(fields=["user", "completed"]),
            models.Index(fields=["user", "status"]),
            models.Index(fields=["due_date"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("todo:list")

    @property
    def is_overdue(self):
        return bool(self.due_date and self.due_date < timezone.localdate() and not self.completed)

    def save(self, *args, **kwargs):
        if self.completed:
            self.status = self.Status.COMPLETED
        elif self.status == self.Status.COMPLETED:
            self.completed = True
        super().save(*args, **kwargs)


class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="activity_logs")
    task = models.ForeignKey(TodoTask, on_delete=models.CASCADE, null=True, blank=True, related_name="activity_logs")
    action = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user}: {self.action}"
