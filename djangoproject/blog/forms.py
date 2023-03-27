from django import forms
from django.forms import ModelForm
from django.forms.widgets import PasswordInput
from .models import *

class RegForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class AuthForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']

class ProfileForm(ModelForm):
    username = forms.CharField(required=False, label='Имя пользователя')
    
    class Meta:
        model = User
        fields = ['username', 'first_name']

class ProfilePhoto(ModelForm):
    class Meta:
        model = Account
        fields = ['photo']

class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']

class AddCommentForm(ModelForm):
    comment = forms.CharField(widget=forms.Textarea, label='Комментарий', required=True)
    class Meta:
        model = Comment
        fields = ['comment']