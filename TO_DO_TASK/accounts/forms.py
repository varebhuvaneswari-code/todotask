from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.models import User

from .models import UserProfile


class BootstrapMixin:
    def apply_bootstrap(self):
        for field in self.fields.values():
            widget = field.widget
            base_class = "form-select" if isinstance(widget, forms.Select) else "form-control"
            widget.attrs["class"] = f"{widget.attrs.get('class', '')} {base_class}".strip()


class SignUpForm(BootstrapMixin, UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Email address"}))
    first_name = forms.CharField(required=False, max_length=30)
    last_name = forms.CharField(required=False, max_length=30)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("placeholder", field.label or name.replace("_", " ").title())

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username


class LoginForm(BootstrapMixin, AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
        self.fields["username"].widget.attrs.update({"placeholder": "Username"})
        self.fields["password"].widget.attrs.update({"placeholder": "Password"})


class ProfileForm(BootstrapMixin, forms.ModelForm):
    first_name = forms.CharField(required=False, max_length=30)
    last_name = forms.CharField(required=False, max_length=30)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ("full_name", "bio", "avatar", "dark_mode")
        widgets = {"bio": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["first_name"].initial = self.user.first_name
        self.fields["last_name"].initial = self.user.last_name
        self.fields["email"].initial = self.user.email
        self.apply_bootstrap()
        self.fields["dark_mode"].widget.attrs["class"] = "form-check-input"

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.exclude(pk=self.user.pk).filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already used by another account.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.email = self.cleaned_data["email"]
        if commit:
            self.user.save()
            profile.save()
        return profile


class StyledPasswordResetForm(BootstrapMixin, PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
        self.fields["email"].widget.attrs.update({"placeholder": "Email address"})


class StyledSetPasswordForm(BootstrapMixin, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class StyledPasswordChangeForm(BootstrapMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
