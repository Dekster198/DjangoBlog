from django.db import models

# Create your models here.
class User(models.Model):
    email = models.TextField
    password = models.TextField
    nickname = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=20, blank=True)
    age = models.IntegerField(blank=True)
    registration_date = models.DateField()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=30)
    text = models.TextField()