from django.shortcuts import render

# Create your views here.

def task(request):
    return render(request, 'task.html')

def login(request):

    return render(request,'login.html')

def signup(request):

    return render(request,'signup.html')
