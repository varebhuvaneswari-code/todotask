from django import forms
from django.utils import timezone

from .models import Category, TodoTask


class TodoTaskForm(forms.ModelForm):
    class Meta:
        model = TodoTask
        fields = ("title", "description", "status", "completed", "due_date", "priority", "category")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Task title"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Add helpful context"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(user=self.user)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters.")
        return title

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if due_date and due_date < timezone.localdate():
            raise forms.ValidationError("Due date cannot be in the past.")
        return due_date


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "color")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category name"}),
            "color": forms.TextInput(attrs={"class": "form-control form-control-color", "type": "color"}),
        }

    def clean_name(self):
        return self.cleaned_data["name"].strip()
