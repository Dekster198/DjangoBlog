from django.contrib import admin
from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('login', login, name='login'),
    path('registration', registration, name='registration'),
    path('new_post', new_post, name='new_post'),
    path('logout', logoutView, name='logout'),
    path('post/<slug:the_slug>', PostComment.as_view(), name='show_post'),
    path('profile', profile, name='profile'),
    path('delete_profile/<str:username>', delete_profile, name='delete_profile'),
]