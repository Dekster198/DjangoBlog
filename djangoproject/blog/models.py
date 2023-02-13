from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/photo/')


# Create your models here.
# class User(models.Model):
#     email = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     nickname = models.CharField(max_length=20)
#     name = models.CharField(max_length=20, blank=True)
#     age = models.IntegerField(null=True)
#     photo = models.ImageField(upload_to='images/photo/')
#     registration_time = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=30)
    text = models.TextField()
