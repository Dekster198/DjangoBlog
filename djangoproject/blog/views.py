from django.shortcuts import render
from django.http import HttpResponse
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    auth_form = AuthRegForm()
    return render(request, 'login.html', context={'form': auth_form})

def registration(request):
    reg_form = AuthRegForm()
    return render(request, 'registration.html', context={'form': reg_form})