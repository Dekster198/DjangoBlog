from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('login', login, name='login'),
    path('registration', RegistrationView.as_view(), name='registration'),
    path('new_post', PostCreateView.as_view(), name='new_post'),
    path('logout', logout_view, name='logout'),
    path('category/<slug:the_slug>', posts_by_category, name='posts_by_category'),
    path('post/<slug:the_slug>', PostComment.as_view(), name='show_post'),
    path('post/<slug:slug>/edit', PostUpdateView.as_view(), name='edit_post'),
    path('profile', Profile.as_view(), name='profile'),
    path('delete_profile/<str:username>', delete_profile, name='delete_profile'),
    path('api/v1/user/', UserAPIListCreate.as_view()),
    path('api/v1/user/<int:pk>/', UserAPIDetailView.as_view()),
    path('api/v1/', include(router.urls)),
]

handler404 = pageNotFound
