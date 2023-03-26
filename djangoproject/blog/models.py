from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .utils import slugify

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='static/images/avatar/', default='static/images/avatar/default_img.jpg', blank=True, verbose_name='Фото профиля')

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, null=False, unique=True, db_index=True)
    text = models.TextField(verbose_name='Текст')
    creation_time = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    comment_time = models.DateTimeField(auto_now_add=True)