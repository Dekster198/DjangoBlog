from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .utils import slugify


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='static/images/avatar/', default='static/images/avatar/default/default_img.jpg', blank=True, verbose_name='Фото профиля')

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=50, null=False, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('posts_by_category', kwargs={'the_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Post(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, null=False, unique=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    text = models.TextField(verbose_name='Текст')
    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('show_post', kwargs={'the_slug': self.slug})

    def get_time_difference(self):
        return (self.update_time - self.creation_time).total_seconds()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    author = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Автор')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    comment_time = models.DateTimeField(auto_now_add=True)
