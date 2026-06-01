from django.shortcuts import render


def home(request):
    return render(request, "core/home.html", {"show_dashboard_cta": request.user.is_authenticated})


def error_404(request, exception):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)
