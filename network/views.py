from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Post
from .serializers import PostSerializer, UserSerializer


def home(request):
    posts = Post.objects.order_by("-modified")
    return render(request, "network/home.html", {"posts": posts})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            # Valid user
            login(request, user)
            return redirect("home")
        else:
            # Wrong credentials
            return render(
                request, "network/login.html", {"message": "Invalid Credentials!"}
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        if not (username and email and password and confirmation and name):
            return render(
                request, "network/register.html", {"message": "Enter all fields"}
            )


        if confirmation != password:
            return render(
                request,
                "network/register.html",
                {"message": "Confirmation password not matched!"},
            )

        [first_name, last_name] = name.split(" ", 1)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
        except IntegrityError:
            return render(
                request,
                "network/register.html",
                {"message": "Username already exists in system!"},
            )

        login(request, user)
        return redirect("home")
    else:
        return render(request, "network/register.html")


def my_posts(request):
    user = request.user
    posts = Post.objects.filter(author__username=user.username).order_by("-modified")
    return render(request, "network/my_posts.html", {"posts": posts, "user": user})


class PostApiView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class UserApiView(APIView):
    def get(self, request, *args, **kwargs):
        username = kwargs["username"]
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
