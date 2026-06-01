from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CategoryForm, TodoTaskForm
from .models import ActivityLog, Category, Priority, TodoTask


def log_activity(user, action, task=None):
    ActivityLog.objects.create(user=user, action=action, task=task)


@login_required
def dashboard(request):
    tasks = TodoTask.objects.filter(user=request.user)
    stats = tasks.aggregate(
        total=Count("id"),
        completed_count=Count("id", filter=Q(completed=True)),
        pending_count=Count("id", filter=Q(completed=False)),
        high=Count("id", filter=Q(priority__name__iexact="High", completed=False)),
    )
    recent_tasks = tasks.select_related("priority", "category")[:6]
    activity = ActivityLog.objects.filter(user=request.user).select_related("task")[:8]
    return render(request, "todo/dashboard.html", {"stats": stats, "recent_tasks": recent_tasks, "activity": activity})


@login_required
def todo_list(request):
    tasks = TodoTask.objects.filter(user=request.user).select_related("priority", "category")
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    priority = request.GET.get("priority", "")
    sort = request.GET.get("sort", "due_date")

    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query))
    if status == "completed":
        tasks = tasks.filter(completed=True)
    elif status == "pending":
        tasks = tasks.filter(completed=False)
    if priority:
        tasks = tasks.filter(priority_id=priority)

    sort_map = {"created": "-created_at", "priority": "priority__level", "due_date": "due_date", "title": "title"}
    tasks = tasks.order_by("completed", sort_map.get(sort, "due_date"), "-created_at")

    paginator = Paginator(tasks, 8)
    context = {
        "page_obj": paginator.get_page(request.GET.get("page")),
        "priorities": Priority.objects.all(),
        "categories": Category.objects.filter(user=request.user),
        "filters": {"q": query, "status": status, "priority": priority, "sort": sort},
    }
    return render(request, "todo/todo_list.html", context)


@login_required
def todo_create(request):
    form = TodoTaskForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        log_activity(request.user, "created a task", task)
        messages.success(request, "Task created successfully.")
        return redirect("todo:list")
    return render(request, "todo/todo_form.html", {"form": form, "category_form": CategoryForm(), "page_title": "Add task"})


@login_required
def todo_update(request, pk):
    task = get_object_or_404(TodoTask, pk=pk, user=request.user)
    form = TodoTaskForm(request.POST or None, instance=task, user=request.user)
    if request.method == "POST" and form.is_valid():
        task = form.save()
        log_activity(request.user, "updated a task", task)
        messages.success(request, "Task updated successfully.")
        return redirect("todo:list")
    return render(request, "todo/todo_form.html", {"form": form, "category_form": CategoryForm(), "task": task, "page_title": "Edit task"})


@login_required
@require_POST
def todo_delete(request, pk):
    task = get_object_or_404(TodoTask, pk=pk, user=request.user)
    title = task.title
    task.delete()
    log_activity(request.user, f"deleted task: {title}")
    messages.success(request, "Task deleted.")
    return redirect("todo:list")


@login_required
@require_POST
def todo_toggle(request, pk):
    task = get_object_or_404(TodoTask, pk=pk, user=request.user)
    task.completed = not task.completed
    if not task.completed and task.status == TodoTask.Status.COMPLETED:
        task.status = TodoTask.Status.PENDING
    task.save()
    log_activity(request.user, "completed a task" if task.completed else "reopened a task", task)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"completed": task.completed, "status": task.get_status_display()})
    messages.success(request, "Task status updated.")
    return redirect("todo:list")


@login_required
@require_POST
def category_create(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        _, created = Category.objects.get_or_create(
            user=request.user,
            name=form.cleaned_data["name"],
            defaults={"color": form.cleaned_data["color"]},
        )
        messages.success(request, "Category added." if created else "That category already exists.")
    else:
        messages.error(request, "Please enter a valid category name.")
    return redirect(request.META.get("HTTP_REFERER", "todo:create"))
