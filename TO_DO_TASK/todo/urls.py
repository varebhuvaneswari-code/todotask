from django.urls import path

from . import views

app_name = "todo"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("", views.todo_list, name="list"),
    path("add/", views.todo_create, name="create"),
    path("<int:pk>/edit/", views.todo_update, name="update"),
    path("<int:pk>/delete/", views.todo_delete, name="delete"),
    path("<int:pk>/toggle/", views.todo_toggle, name="toggle"),
    path("categories/add/", views.category_create, name="category_create"),
]
