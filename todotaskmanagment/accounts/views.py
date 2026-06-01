from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render

from .forms import LoginForm, ProfileForm, SignUpForm


class RememberMeLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember = form.cleaned_data.get("remember_me")
        self.request.session.set_expiry(60 * 60 * 24 * 30 if remember else 0)
        messages.success(self.request, "Welcome back. Your workspace is ready.")
        return super().form_valid(form)


def signup(request):
    if request.user.is_authenticated:
        return redirect("todo:dashboard")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                user = form.save()
                user.profile.full_name = f"{user.first_name} {user.last_name}".strip()
                user.profile.save(update_fields=["full_name", "updated_at"])
        except IntegrityError:
            form.add_error(None, "This account could not be created because the username or email is already in use.")
            return render(request, "accounts/signup.html", {"form": form})
        login(request, user)
        messages.success(request, "Account created successfully. Let's plan the day.")
        return redirect("todo:dashboard")
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"form": form})
