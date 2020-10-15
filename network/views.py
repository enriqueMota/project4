import json
import datetime
from django import forms
from django.urls import reverse
from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .models import User, Follow, Post, Like

class NewPost(forms.Form):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'autocomplete':'off','class':'form-control','placeholder':'Write your post here', 'id':'blody', 'rows':'4'}))


def index(request):

    if request.user.is_authenticated:    


        posts = Post.objects.all()
        posts = posts.order_by("-timestamp").all()

        all_likes = Like.objects.all()
        liked_posts = set()

        for like in all_likes:
            if request.user.username == like.user.username:
                liked_posts.add(like.post.id)

        if posts.count() > 10:

            paginator = Paginator(posts, 10)
            page_numer = request.GET.get('page')
            page_obj = paginator.get_page(page_numer)

            page_links = range(1, page_obj.paginator.num_pages + 1)

            return render(request, "network/index.html", {
                "logged": True,
                'newPost': NewPost(),
                'posts': page_obj,
                'page_links': page_links,
                'likes': liked_posts
            })

        elif posts.count() <= 10:

            return render(request, "network/index.html", {
                "logged": True,
                'newPost': NewPost(),
                'posts': posts,
                'likes':liked_posts
            })
    else:
        return HttpResponseRedirect(reverse('login'))

def new_post(request):
    return render(request, 'network/new_post.html',{
        'newPost':NewPost()
    })

def post(request):
    if request.method == 'POST':

        if NewPost(request.POST):
            submition = NewPost(request.POST)
            author = User.objects.get(username=request.user)
            if submition.is_valid():
                body = submition.cleaned_data['body']
                p = Post.objects.create(author=author, body=body)
                p.save()
                return HttpResponseRedirect(reverse('index'))
        else:
            return JsonResponse({"None":"True"})


    elif request.method == 'GET':
        return JsonResponse({"Wrong method":"man"})

    data = json.loads(request.body)
    identity = int(data.get("id"))
    edition = data.get("body")

    edited = Post.objects.get(pk=identity)

    edited.body = edition
    edited.save()
    return JsonResponse({"Post updated":"successfully"})

def profile(request, username):
    
    # All followers
    followers = User.objects.get(username=f"{username}").followers.all().count()

    # All following
    following = User.objects.get(username=f"{username}").following.all().count()

    # All follows
    follow_list = Follow.objects.all()

    # All posts
    profile_posts =  Post.objects.filter(author=User.objects.get(username=f'{username}'))

    # Reverse chronologically ordered posts
    profile_posts = profile_posts.order_by('-timestamp').all()

    # All likes
    all_likes = Like.objects.all()
    
    # Checking if the user liked a post
    liked_posts = set()
    for like in all_likes:
        if request.user.username == like.user.username:
            liked_posts.add(like.post.id)

    # Checking if the user follows the visible profile
    account = []
    for z in follow_list:
        if z.follower == User.objects.get(username=f'{request.user}') and z.followed == User.objects.get(username=f'{username}'):
            account.append(z)

    if len(account) == 1:

        if profile_posts.count() > 10:

            paginator = Paginator(profile_posts, 10)
            page_numer = request.GET.get('page')
            page_obj = paginator.get_page(page_numer)

            page_links = range(1, page_obj.paginator.num_pages + 1)

            return render(request, "network/profile.html", {
                "logged": True,
                'newPost': NewPost(),
                'posts': page_obj,
                'page_links': page_links,
                'followers':followers,
                'following':following,
                'username':username,
                'follows': account,
                'likes': liked_posts
            })
        elif profile_posts.count() < 10:

            return render(request, 'network/profile.html',{
                'logged': True,
                'username':username,
                'newPost': NewPost(),
                'followers': followers,
                'following': following,
                'posts':profile_posts,
                'follows':account,
                'likes': liked_posts
            })

    else:
        if profile_posts.count() > 10:

            paginator = Paginator(profile_posts, 10)
            page_numer = request.GET.get('page')
            page_obj = paginator.get_page(page_numer)

            page_links = range(1, page_obj.paginator.num_pages + 1)

            return render(request, "network/profile.html", {
                "logged": True,
                'newPost': NewPost(),
                'posts': page_obj,
                'page_links': page_links,
                'followers':followers,
                'following':following,
                'username':username,
                'likes': liked_posts
            })
        elif profile_posts.count() < 10:

            return render(request, 'network/profile.html',{
                'logged': True,
                'username':username,
                'newPost': NewPost(),
                'followers': followers,
                'following': following,
                'posts':profile_posts,
                'likes': liked_posts
            })

def follow(request, username):

    if request.method == 'GET':
        return HttpResponseRedirect(reverse('index'))

    follow = Follow.objects.create(follower=User.objects.get(username=f'{request.user}'),followed=User.objects.get(username=username))
    follow.save()
    return JsonResponse({"Followed":"Successfully"})

def unfollow(request,username):
    
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('index'))

    unfollow = Follow.objects.get(follower=User.objects.get(username=f'{request.user}'), followed=User.objects.get(username=username))
    unfollow.delete()
    return JsonResponse({"Un":"Followed"})

def like(request, post_id):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('index'))
    
    liking = Like.objects.create(user=User.objects.get(username=f'{request.user}'), post=Post.objects.get(pk=post_id))
    liking.save()
    return JsonResponse({"Liked":"Successfully"})

def dislike(request, post_id):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('index'))

    disliking = Like.objects.get(post=Post.objects.get(pk=post_id))
    disliking.delete()
    return JsonResponse({"disliked":"Successfully"})

def following(request, username):

    if request.method != 'POST':
        if request.user.is_authenticated:
            user = User.objects.get(username=username)
            follows = user.following.all()
            all_likes = Like.objects.all()
            liked_posts = set()

            for like in all_likes:
                if request.user.username == like.user.username:
                    liked_posts.add(like.post.id)

            posts_array = []
            for z in follows:
                m = Post.objects.filter(author= z.followed)
                if m.count() == 1:
                    for a in m:
                        posts_array.append(a)
                elif m.count() > 1:
                    for x in m:
                        posts_array.append(x)
            omega = sorted(posts_array, key=lambda x: x.timestamp, reverse=True)
            
            if len(omega) > 10:
                
                paginator = Paginator(omega, 10)
                page_numer = request.GET.get('page')
                page_obj = paginator.get_page(page_numer)

                page_links = range(1, page_obj.paginator.num_pages + 1)

                return render(request, 'network/following.html', {
                    "all_posts": page_obj,
                    "logged": True,
                    "page_links": page_links,
                    "posts": page_obj,
                    "likes": liked_posts
                })
            elif len(omega) < 10:

                return render(request, 'network/following.html',{
                    "all_posts": omega,
                    "logged": True,
                    "likes": liked_posts
                })
        return HttpResponseRedirect(reverse('index'))

def login_view(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
