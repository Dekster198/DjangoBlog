from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from rest_framework import viewsets, routers, generics
from rest_framework import permissions
from .serializers import *
from .permissions import *
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

class RegistrationView(CreateView):
    form_class = RegForm
    template_name = 'registration.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reg_form'] = context['form']

        return context

    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        user = form.save()
        account = Account.objects.create(user=user)
        account.save()

        return super().form_valid(form)

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
            messages.add_message(request, messages.INFO, 'Неправильное имя пользователя или пароль')
            return redirect('login')
    else:
        auth_form = AuthForm()
    return render(request, 'login.html', context={'auth_form': auth_form})

def logoutView(request):
    logout(request)
    return redirect('home')

class PostCreateView(CreateView):
    form_class = AddPostForm
    template_name = 'new_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_form'] = context['form']

        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Account.objects.get(user=User.objects.get(username=self.request.user))
        post.save()

        return super().form_valid(form)

class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'text')
    template_name = 'edit_post.html'

class PostComment(View):
    def get(self, request, the_slug):
        post = get_object_or_404(Post, slug=the_slug)
        comments = Comment.objects.filter(post=post).order_by('-comment_time')
        comment_form = AddCommentForm()

        return render(request, 'post.html', context={'title': post.title, 'slug': post.slug, 'text': post.text,
                                                 'author': post.author, 'creation_time': post.creation_time,
                                                 'update_time': post.update_time, 'time_difference': post.get_time_difference(),
                                                 'comment_form': comment_form, 'comments': comments})
    
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

class Profile(View):
    def get(self, request):
        profile_form = ProfileForm()
        profile_photo = ProfilePhoto()
        username = request.user
        name = User.objects.get(username=username)
        acc = Account.objects.get(user=User.objects.get(username=username))

        return render(request, 'profile.html', context={'acc': acc, 'username': username, 'name':name.first_name, 'profile_form': profile_form, 
                                                    'profile_photo': profile_photo})
    
    def post(self, request):
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

            return redirect('profile')

        return render(request, 'profile.html', context={'profile_form': profile_form, 
                                                    'profile_photo': profile_photo})

def delete_profile(request, username):
    if username == str(request.user):
        user = User.objects.get(username=request.user)
        logout(request)
        user.delete()
        return redirect('home')

class UserAPIListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrIsNotAuth, )

class UserAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrIsAdminOrReadOnly, )

class AccountViewset(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsOwnerOrIsAdminOrReadOnly, )

class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrIsAdminOrReadOnly, )

class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrIsAdminOrReadOnly, )

router = routers.SimpleRouter()
router.register('account', AccountViewset)
router.register('post', PostViewset)
router.register('comment', CommentViewset)