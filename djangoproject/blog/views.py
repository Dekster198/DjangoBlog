from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            email = auth_form.cleaned_data['email']
            password = auth_form.cleaned_data['password']
            if User.objects.filter(email=email, password=password):
                return redirect('home')
            else:
                return redirect('registration')
    else:
        auth_form = AuthForm()
        return render(request, 'login.html', context={'form': auth_form})

def registration(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            return redirect('home')
    else:
        reg_form = RegForm()
        return render(request, 'registration.html', context={'form': reg_form})