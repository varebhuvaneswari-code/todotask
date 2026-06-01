from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountFlowTests(TestCase):
    def test_signup_creates_user_and_profile(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "demo",
                "email": "demo@example.com",
                "first_name": "Demo",
                "last_name": "User",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertRedirects(response, reverse("todo:dashboard"))
        user = User.objects.get(username="demo")
        self.assertTrue(hasattr(user, "profile"))

    def test_login_page_renders(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Remember me")
