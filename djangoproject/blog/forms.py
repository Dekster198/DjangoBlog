from django import forms
from django.forms import ModelForm
from django.forms.widgets import PasswordInput
from .models import *

class RegForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            self.add_error('email', 'Эта почта уже зарегистрирована')

        return cleaned_data

class AuthForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
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
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 150, 'style': 'resize: none'}), label='', required=True)
    class Meta:
        model = Comment
        fields = ['comment']