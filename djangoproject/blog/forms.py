from django import forms
from django.forms import ModelForm
from django.forms.widgets import PasswordInput
from .models import *

class AuthRegForm(ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'email', 'password']

class UserForm(forms.ModelForm):
    class Meta:
        nickname = forms.CharField()
        name = forms.CharField()
        age = forms.IntegerField()