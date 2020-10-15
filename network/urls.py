
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('post', views.post, name='post'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('new_post', views.new_post, name='new_post'),
    path("register", views.register, name="register"),
    path('like/<int:post_id>', views.like, name='like'),
    path('dislike/<int:post_id>', views.dislike, name='like'),
    path('user/<str:username>', views.profile, name='profile'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('unfollow/<str:username>', views.unfollow, name='unfollow'),
    path('user/<str:username>/following', views.following, name='following'),

]
