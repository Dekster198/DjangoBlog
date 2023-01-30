from django import forms
from django.forms.widgets import PasswordInput

class AuthRegForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=PasswordInput)

class UserForm(forms.Form):
    nickname = forms.CharField()
    name = forms.CharField()
    age = forms.IntegerField()