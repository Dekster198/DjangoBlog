from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .utils import slugify

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/photo/')

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=255, null=False, unique=True, db_index=True)
    text = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)