from django import forms
from django.forms import ModelForm, Form
from django.forms.widgets import PasswordInput
from django.core.mail import send_mail

from .models import *
from .tasks import send_feedback_email_task


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


class ProfileFormFromUser(ModelForm):
    username = forms.CharField(required=False, label='Имя пользователя')
    
    class Meta:
        model = User
        fields = ['username', 'first_name']


class ProfileForm(ModelForm):
    birthday = forms.DateField(required=False, label='День рождения')

    class Meta:
        model = Account
        fields = ['birthday', 'photo']


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'text']


class AddCommentForm(ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 150, 'style': 'resize: none'}), label='', required=True)

    class Meta:
        model = Comment
        fields = ['comment']

class FeedbackForm(Form):
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 150, 'style': 'resize: none'}), label='Сообщение', required=True)

    def send_email(self):
        print('Отправка сообщения')
        send_feedback_email_task.delay(
            self.cleaned_data['email'],
            self.cleaned_data['message']
        )