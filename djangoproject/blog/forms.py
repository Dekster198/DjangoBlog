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

class UserForm(forms.ModelForm):
    class Meta:
        nickname = forms.CharField()
        name = forms.CharField()
        age = forms.IntegerField()

class AddPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']