from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Priority, TodoTask


class TodoFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="demo", password="StrongPass123!")
        self.priority = Priority.objects.get(name="High")
        self.client.force_login(self.user)

    def test_create_update_toggle_delete_task(self):
        create_response = self.client.post(
            reverse("todo:create"),
            {
                "title": "Prepare release notes",
                "description": "Summarize completed work",
                "status": TodoTask.Status.PENDING,
                "due_date": timezone.localdate(),
                "priority": self.priority.pk,
            },
        )
        self.assertRedirects(create_response, reverse("todo:list"))
        task = TodoTask.objects.get(title="Prepare release notes")

        update_response = self.client.post(
            reverse("todo:update", args=[task.pk]),
            {
                "title": "Prepare launch notes",
                "description": "Summarize completed work",
                "status": TodoTask.Status.IN_PROGRESS,
                "due_date": timezone.localdate(),
                "priority": self.priority.pk,
            },
        )
        self.assertRedirects(update_response, reverse("todo:list"))
        task.refresh_from_db()
        self.assertEqual(task.title, "Prepare launch notes")

        toggle_response = self.client.post(reverse("todo:toggle", args=[task.pk]))
        self.assertRedirects(toggle_response, reverse("todo:list"))
        task.refresh_from_db()
        self.assertTrue(task.completed)

        delete_response = self.client.post(reverse("todo:delete", args=[task.pk]))
        self.assertRedirects(delete_response, reverse("todo:list"))
        self.assertFalse(TodoTask.objects.filter(pk=task.pk).exists())

    def test_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("todo:list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)
