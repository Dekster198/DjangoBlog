from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    auth_form = AuthRegForm()
    return render(request, 'login.html', context={'form': auth_form})

def registration(request):
    if request.method == 'POST':
        reg_form = AuthRegForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            messages.success(request, 'Аккаунт успешно создан')
            return redirect('home')
    else:
        reg_form = AuthRegForm(request.POST)
        return render(request, 'registration.html', context={'form': reg_form})