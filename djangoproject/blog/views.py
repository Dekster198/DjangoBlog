from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def registration(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        user.save()
        return redirect('home')
    else:
        reg_form = RegForm()
        return render(request, 'registration.html', context={'reg_form': reg_form})

def login(request):
    if request.method == 'POST':
        auth_form = AuthForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Oops...')
    else:
        auth_form = AuthForm()
    return render(request, 'login.html', context={'auth_form': auth_form})

def logoutView(request):
    logout(request)
    return redirect('home')

def newPost(request):
    if request.method == 'POST':
        user = request.user.username
        print(user)
        post_form = AddPost(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect('home')
    else:
        post_form = AddPost()
        return render(request, 'new_post.html', context={'post_form': post_form})