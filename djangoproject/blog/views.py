from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        auth_form = AuthForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            return HttpResponse(f'Hello, {user}')
        else:
            return HttpResponse('Oops...')
    else:
        auth_form = AuthForm()
    return render(request, 'login.html', context={'auth_form': auth_form})

def registration(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            return redirect('home')
    else:
        reg_form = RegForm()
        return render(request, 'registration.html', context={'reg_form': reg_form})