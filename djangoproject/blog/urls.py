from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('login', login, name='login'),
    path('registration', registration, name='registration'),
    path('new_post', new_post, name='new_post'),
    path('logout', logoutView, name='logout'),
    path('post/<slug:the_slug>', show_post, name='show_post'),
]