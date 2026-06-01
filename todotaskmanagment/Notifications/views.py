from django.shortcuts import render

# Create your views here.
def notifi(request):
    return render(request, 'notifi.html')

