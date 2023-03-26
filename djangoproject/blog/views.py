from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import View
from .models import *
from .forms import *

# Create your views here.
def index(request):
    try:
        posts = Post.objects.all()
        user = User.objects.get(username=request.user)
        acc = Account.objects.get(user=user)
        
        return render(request, 'index.html', context={'posts': posts, 'acc': acc})
    except User.DoesNotExist:
        user=None
    
    return render(request, 'index.html')

def registration(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        user.save()
        account = Account.objects.create(user=user)
        account.save()
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

def new_post(request):
    if request.method == 'POST':
        post_form = AddPostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post_form.save()

            return redirect('home')
    else:
        post_form = AddPostForm()
        return render(request, 'new_post.html', context={'post_form': post_form})

class PostComment(View):
    def get(self, request, the_slug):
        post = get_object_or_404(Post, slug=the_slug)
        comments = Comment.objects.all().order_by('-comment_time')
        comment_form = AddCommentForm()

        return render(request, 'post.html', context={'title': post.title, 'text': post.text, 
                                                 'author': post.author, 'creation_time': post.creation_time, 'comment_form': comment_form,
                                                 'comments': comments})
    
    def post(self, request, the_slug):
        comment_form = AddCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.cleaned_data['comment']
            post = Post.objects.get(slug=the_slug)
            author = Account.objects.get(user=request.user)
            comment = Comment.objects.create(post=post, author=author, comment=user_comment)
            comment.save()

            return redirect(reverse('show_post', kwargs={'the_slug': the_slug}))
        
        return render(request, 'post.html', context={'comment_form': comment_form})

def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        profile_photo = ProfilePhoto(request.POST, request.FILES)
        if profile_form.is_valid() and profile_photo.is_valid():
            user = User.objects.get(username=request.user)
            acc = Account.objects.get(user=user)
            if profile_form.cleaned_data['username'] != '':
                username = profile_form.cleaned_data['username']
                user.username = username
            if profile_form.cleaned_data['first_name'] != '':
                first_name = profile_form.cleaned_data['first_name']
                user.first_name = first_name
            if profile_photo.cleaned_data['photo'] is not None:
                photo = profile_photo.cleaned_data['photo']
                acc.photo = photo
            user.save()
            acc.save()
    else:
        profile_form = ProfileForm()
        profile_photo = ProfilePhoto()
    return render(request, 'profile.html', context={'profile_form': profile_form, 
                                                    'profile_photo': profile_photo})